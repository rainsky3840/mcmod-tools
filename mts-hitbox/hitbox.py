import re, json, os, math

print('▶▶ MQO TO MTS HITBOX EXPORTER / made by Rainwind ◀◀')
while True:
  try:
    model_fp = input('▶ Open MQO file: ') + '.mqo'
    with open(model_fp, 'r', encoding='utf-8') as infp:
      text = infp.read()
      print(f'▷ Successfully opened {model_fp} file!')
    # Find vertices from mqo file based on object name
    while True:
      try:
        object_name = input('▶ Object name for hitboxes: ')
        vertex_block = re.search(r'Object\s\"' + re.escape(object_name) + '\"\s{[\s\S]+?vertex\s\d+\s{([\d\D]*?)}', text).group(1).strip()
        vertex_lines = vertex_block.split('\n')
        vertices = [list(map(float, line.strip().split())) for line in vertex_lines]
        print(f'▷ Found object: {object_name}')
        break
      except AttributeError:
        print(f'▷ Cannot find the specified object!')
    break
  except FileNotFoundError:
    print('▷ Failed to open a valid file!')

# A prism has 8 vertices. Divide and group by 8, store in list
hitboxes= []
for idx, point in enumerate(vertices):
  if (idx+1) % 8 == 0:
    hitboxes.append(vertices[idx-7 : idx+1])

# Calculate distance between two points in 3D space
def distance3D(p1, p2):
  dx = p2[0] - p1[0]
  dy = p2[1] - p1[1]
  dz = p2[2] - p1[2]
  distance = math.sqrt(dx**2 + dy**2 + dz**2)
  return round(distance/100, 4)

# Get center of each hitbox
def get_center(points):
    x_sum = 0
    y_sum = 0
    z_sum = 0

    for point in points:
        x_sum += point[0]
        y_sum += point[1]
        z_sum += point[2]
    
    mean_x = x_sum / 8
    mean_y = y_sum / 8
    mean_z = z_sum / 8
    
    return [round(mean_x/100, 4), round(mean_y/100, 4), round(mean_z/100, 4)]

# Get length, width, height, center point of each hitbox
def calc_dimensions(hitbox):
  length = distance3D(hitbox[0], hitbox[6])
  width = distance3D(hitbox[0], hitbox[2])
  height = distance3D(hitbox[0], hitbox[1])
  return [length, width, height]

# Store hitbox size and position info
json_str = '''
{
  "collisionGroups": [
    {
      "collisions": [
      ]
    }
  ]
}
'''
json_obj = json.loads(json_str)

# Convert to MTS-friendly JSON format
for idx, each in enumerate(hitboxes):
  print(f'HITBOX {idx} / Center: {get_center(each)} / Dimensions(LWH): {calc_dimensions(each)}')
  json_obj['collisionGroups'][0]['collisions'].append({
    "pos": get_center(each),
    "width": calc_dimensions(each)[1],
    "height": calc_dimensions(each)[2]
  })

# "pos" values in json are on a single line
pattern = re.compile(r'"pos":\s\[\n\s+(-?\d+.?\d+?),\n\s+(-?\d+.?\d+?),\n\s+(-?\d+.?\d+?)\n\s+]')
def prettify(match):
  return f"\"pos\": [{match.group(1)}, {match.group(2)}, {match.group(3)}]"
json_formatted = pattern.sub(prettify, json.dumps(json_obj, indent=2))

while True:
  savechoice = input('▶ Export Options: View(1) / Save(2) / Exit(press other key): ')
  if savechoice == '1':
    print(pattern.sub(prettify, json.dumps(json_obj, indent=2)))
  elif savechoice == '2':
    export_fp = input('▶ Input name to save as new file: ') + '.json'
    # Overwrite operation: add json block as new collisionGroup
    if os.path.isfile(export_fp) == True:
      while True:
        print('▷ Existing file found! Adding new collisionGroup will overwrite current JSON file and might result in potential data loss!')
        overwrite_reminder = input('▶ Continue operation(1) / Exit(press other key): ')
        if overwrite_reminder == '1':
          try:
            with open(export_fp, 'r') as addfp:
              json_ori = json.load(addfp)
            json_ori['collisionGroups'].append(json_obj['collisionGroups'][0])
            json_added = pattern.sub(prettify, json.dumps(json_ori, indent=2))
            with open(export_fp, 'w') as replacefp:
              replacefp.write(json_added)
            print(f'▷ A new collisionGroup has been added to {export_fp}')
            addfp.close()
            replacefp.close()
            break
          except:
            print(f'▷ Error! Is it a valid MTS JSON?')
            addfp.close()
            break
        else:
          print('▷ Overwrite operation cancelled!')
          break
    else:
      with open(export_fp, 'w') as outfp:
        outfp.write(json_formatted)
      print(f'▷ JSON file exported as {export_fp}')
      outfp.close()
  else:
    infp.close()
    print('▷ Operation completed! Shutting down...')
    break