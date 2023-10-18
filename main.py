import vec3d, re

searchlist1 = ['AddFixedSearchLight', 'AddPartCamera', 'AddPartCanopy', 'AddPartHatch', 'AddPartLG', 'AddPartLGHatch', 'AddPartLGRev', 'AddPartLightHatch', 'AddPartNozzle', 'AddPartRotation', 'AddPartRotor', 'AddPartSlideHatch', 'AddPartSteeringWheel', 'AddPartThrottle', 'AddPartWheel', 'AddPartWing', 'AddParticleSplash', 'AddRepellingHook', 'AddSearchLight', 'AddSeat', 'AddSteeringSearchLight', 'BoundingBox', 'CameraPosition', 'TurretPosition']
searchlist2 = ['AddWeapon', 'AddPartWeaponBay', 'AddPartSlideWeaponBay', 'AddRack']
searchlist3 = ['AddGunnerSeat', 'AddPartSlideRotLG']
searchlist4 = ['AddPartWeaponMissile', 'AddPartRotWeapon', 'AddPartTurretWeapon', 'AddPartWeaponChild', 'AddPartWeapon']
searchlist5 = ['AddBlade', 'AddRotor']

# 1. Name = (0.0, 0.0, 0.0)
pattern1 = r'=\s*([-+]?\d+\.?\d*,\s*[-+]?\d+\.?\d*,\s*[-+]?\d+\.?\d*)'
# 2. Name = weapon [optional]/weapon/weapon, (0.0, 0.0, 0.0), [optional](0.0, 0.0, 0.0)
pattern2 = r'\w+\s*=\s*(?:[\w\/\s-]+,)?\s*([-+]?\d+\.?\d*,\s*[-+]?\d+\.?\d*,\s*[-+]?\d+\.?\d*),?\s*([-+]?\d+\.?\d*,\s*[-+]?\d+\.?\d*,\s*[-+]?\d+\.?\d*)?'
# 3. Name = (0.0, 0.0, 0.0), [optional](0.0, 0.0, 0.0)
pattern3 = r'=\s*([-+]?\d+\.?\d*,\s*[-+]?\d+\.?\d*,\s*[-+]?\d+\.?\d*),?\s*([-+]?\d+\.?\d*,\s*[-+]?\d+\.?\d*,\s*[-+]?\d+\.?\d*)?'
# 4. Name = true, false, [optional]true, (0.0, 0.0, 0.0)
pattern4 = r'\w+\s*=\s*[\w\/\s-]+,\s*(?:false,\s*|true,\s*){1,3}([-+]?\d+\.?\d*,\s*[-+]?\d+\.?\d*,\s*[-+]?\d+\.?\d*)'
# 5. Name = Parameter = 1, 0, (0.0, 0.0, 0.0)
pattern5 = r'\w+\s*=\s*[-+]?\d+\s*,\s*[-+]?\d+\s*,\s*([-+]?\d+\.?\d*,\s*[-+]?\d+\.?\d*,\s*[-+]?\d+\.?\d*)'

#lists of parameters, patterns to loop
searchlists = [searchlist1, searchlist2, searchlist3, searchlist4, searchlist5]
patterns = [pattern1, pattern2, pattern3, pattern4, pattern5]
headers = []

#compile headers
for i in range(len(searchlists)):
  header_new = re.compile(fr"^{'|'.join(searchlists[i])}\s*=")
  headers.append(header_new)

#list to string function: ['a, b, c'] => [a, b, c] format
def list2str(found):
    all_list = []
    # all_str = []
    for idx, each in enumerate(found):
        curr_list = [float(j) for j in found[idx].replace(' ','').split(',')]
        # curr_str = (', '.join(str(k) for k in curr_list))
        all_list.append(curr_list)
        # all_str.append(curr_str)
    return all_list

def calc(vector):
  if choice == '1':
    v_cur = vec3d.Vector3D(vector)
    v_ori = vec3d.Vector3D(ori)
    v_result = v_cur.__scale__(v_ori, scal)
    print(f'Calculated: {vector} => Scale {scal}x => [{v_result}]')
    return v_result
  elif choice == '2':
    v_cur = vec3d.Vector3D(vector)
    v_move = vec3d.Vector3D(move)
    v_result = v_cur.__move__(v_move)
    print(f'Calculated: {vector} => Move => [{v_result}]')
    return v_result

print('▶▶ MCHELI CONFIG RESIZER - MADE BY RAINWIND ◀◀')

#open file
while True:
  try:
    openfile = input('>> Open file (can include directory, don\'t include .txt): ') + '.txt'
    with open(openfile, 'r', encoding='utf-8') as infp:
      text = infp.readlines()
    print('** Successfully opened ', openfile)
    break
  except FileNotFoundError:
    print('** File not found! Please try a different file.')

#get scale/move variables
while True:
  try:
    choice = input('>> 1. Scale / 2. Move : ')
    if choice == '1':
      ori = list(map(float, input('>> Origin (x,y,z): ').replace(' ', '').split(',')))
      scal = float(input('>> Scalar: ').replace(' ', ''))
      print('** Scaling numbers:', ori, scal)
      break
    elif choice == '2':
      move = list(map(float, input('>> Move: ').replace(' ', '').split(',')))
      print('** Moving numbers:', move)
      break
    else:
      print('** Please choose between 1(Scale) and 2(Move)!')
  except:
    print('** Error Encountered! Please input correctly.')
print('')

#main loop
for line_idx, line in enumerate(text):
  for (head, ptn) in zip(headers, patterns):
    if head.match(line):
      print(f'Line {line_idx} : {line.strip()}')
      # print('Matching Header:', head.match(line).group())
      matches = re.findall(ptn, line)
      
      #single match: ['a,b,c'] / multiple matches: [('a,b,c','a,b,c')]
      if (matches[0]).__class__ == tuple:
          matches = list(matches[0])
      
      #format matches to [[a,b,c], [a,b,c]]
      matches = [i for i in matches if i != '']
      # print(matches, type(matches))
      matches_list = list2str(matches)
      # print('Formatted:', matches, '=>', matches_list)
      
      #get calculation results. stores multiple matches in one line.
      calc_results = []
      for idx, each in enumerate(matches_list):
        calc_result = calc(each) 
        calc_results.append(calc_result) 
      # print(f'Converted: {matches} => {calc_results}')
      
      #replace old coordinates w/ new ones
      for (old_str, new_str) in zip(matches, calc_results):
        line = line.replace(old_str, new_str, 1)
        # print('LOOP:', line, end='')
      
      #push changes to main text body
      text[line_idx] = line
      print('FINAL:', line, end='')
      print()

#save, view, and exit
print('** OPERATION COMPLETED')
while True:
  savechoice = input('>> Save File(S) / View File(V) / Working Parameters(W) / Exit Program: ')
  if savechoice in ('W', 'w'):
    all_params=[]
    for i in searchlists:
      all_params.extend(i)
      all_params.sort()
    print('** Parameters supported: ', all_params)
  elif savechoice in ('V', 'v'):
    for each in text:
      print(each, end='')
    print('')
  elif savechoice in ('S', 's'):
    try:
      savefile = input('>> Save file name (can include directory, without .txt): ') + '.txt'
      with open(savefile, 'w', encoding="utf-8") as outfp:
        for line in text:
          outfp.write(line)
        print('** Ending program. Data saved to', savefile)
        infp.close()
        outfp.close()
        break
    except:
      print('** Error saving file. Did you input a valid file path?')
  else:
    print('** ENDING PROGRAM')
    infp.close()
    break