import re, json, os

class Calculate:
  def __init__(self, p1, p2):
    self.p1 = p1
    self.p2 = p2

  def getCenter(self):
    self.dx = self.p1[0] + (self.p2[0] - self.p1[0])/2
    self.dy = self.p1[1] + (self.p2[1] - self.p1[1])/2
    self.dz = self.p1[2] + (self.p2[2] - self.p1[2])/2
    return [self.dx*0.0625, self.dy*0.0625, self.dz*0.0625]
  
  def getDimensions(self):
    self.dx = self.p2[0] - self.p1[0]
    self.dy = self.p2[1] - self.p1[1]
    self.dz = self.p2[2] - self.p1[2]
    return [self.dx*0.0625, self.dy*0.0625, self.dz*0.0625]

print('# Blockbench to MTS Hitbox Exporter - Rainwind')
while True:
  import_fp = input('>> Open bbmodel file(don\'t include file extension): ') + '.bbmodel'
  try:
    with open(import_fp, 'r', encoding='utf-8') as infp:
      data = json.load(infp)
      print(f'Successfully opened {import_fp} file!')
    break
  except:
    print('Error loading file, or file doesn\'t exist!')

group_objects = []
group_name = input('>> Group/bone name for hitboxes: ')
for i in range(len(data['outliner'])):
  try:
    if data['outliner'][i]['name'] == group_name:
      print(f'Group/bone name {group_name} found!')
      for j in data['outliner'][i]['children']:
        group_objects.append(j)
  except:
    if i == len(data['outliner'])-1 and group_objects == []:
      print('Cannot find group/bone name!')
# print(group_objects)

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
new_json = json.loads(json_str)

for i in range(len(data['elements'])):
  object = data['elements'][i]
  if object['uuid'] in group_objects and object['type']=='cube':
    # print(object['uuid'])
    calc = Calculate(object['from'], object['to'])
    position = calc.getCenter()
    width = calc.getDimensions()[0] # width == length
    height = calc.getDimensions()[1]
    print(f'POSITION: {position}, WIDTH: {width}, HEIGHT: {height}')
    new_json["collisionGroups"][0]["collisions"].append({
      "pos": position,
      "width": width,
      "height": height
    })

pattern = re.compile(r'"pos":\s\[\n\s+(-?\d+.?\d+?),\n\s+(-?\d+.?\d+?),\n\s+(-?\d+.?\d+?)\n\s+]')
def prettify(match):
  return f"\"pos\": [{match.group(1)}, {match.group(2)}, {match.group(3)}]"
json_format = pattern.sub(prettify, json.dumps(new_json, indent=2))

while True:
  save_choice = input('>> Export Options: View(1) / Save(2) / Exit(Any other key): ')
  if save_choice == '1':
    print(json_format)
  elif save_choice == '2':
    export_fp = input('>> Name to save as new JSON file: ') + '.json'
    if os.path.isfile(export_fp) == True:
      print('Existing file found! Operation aborted!')
    else:
      with open(export_fp, 'w') as outfp:
        outfp.write(json_format)
        print('File saved as', export_fp)
        outfp.close()
  else:
    print('Closing without any operations')
    infp.close()
    outfp.close()
    break