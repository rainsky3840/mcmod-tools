import math, json, re

doc = MQSystem.getDocument()
num = doc.numObject

class ObjectDialog(MQWidget.Dialog):
	def radioBtn1Callback(self, sender):
		self.modselectflag = 1
		self.radiobtn2.checked = False
		self.radiobtn3.checked = False
	def radioBtn2Callback(self, sender):
		self.modselectflag = 2
		self.radiobtn1.checked = False
		self.radiobtn3.checked = False
	def radioBtn3Callback(self, sender):
		self.modselectflag = 3
		self.radiobtn1.checked = False
		self.radiobtn2.checked = False
		
	def __init__(self, parent):
		MQWidget.Dialog.__init__(self, parent)
		self.title = "MQO Hitbox Exporter"
		self.frame1 = self.createHorizontalFrame(self)
		self.label1 = MQWidget.Label(self.frame1)
		self.label1.text = "Object Name"
		self.edit = MQWidget.Edit(self.frame1)
		self.checkbox1 = MQWidget.CheckBox(self.frame1)
		self.checkbox1.text = "Debug Info"
		self.checkbox1.checked = False
		
		self.frame2 = self.createHorizontalFrame(self)
		self.frame2.uniformSize = True
		self.label3 = MQWidget.Label(self.frame2)
		self.label3.text = "Mod Name"
		self.modselectflag = 1
		self.radiobtn1 = MQWidget.RadioButton(self.frame2)
		self.radiobtn1.text = "MCHeli"
		self.radiobtn1.checked = True
		self.radiobtn1.addChangedEvent(self.radioBtn1Callback)
		self.radiobtn2 = MQWidget.RadioButton(self.frame2)
		self.radiobtn2.text = "IA"
		self.radiobtn2.checked = False
		self.radiobtn2.addChangedEvent(self.radioBtn2Callback)
		self.radiobtn3 = MQWidget.RadioButton(self.frame2)
		self.radiobtn3.text = "MTS"
		self.radiobtn3.checked = False
		self.radiobtn3.addChangedEvent(self.radioBtn3Callback)
		
		self.frame3 = self.createHorizontalFrame(self)
		self.frame3.uniformSize = True			
		self.okbtn = MQWidget.Button(self.frame3)
		self.okbtn.text = MQSystem.getResourceString("OK")
		self.okbtn.modalResult = "ok"
		self.okbtn.default = 1
		self.okbtn.fillBeforeRate = 1
		self.cancelbtn = MQWidget.Button(self.frame3)
		self.cancelbtn.text = MQSystem.getResourceString("Cancel")
		self.cancelbtn.modalResult = "cancel"
		self.cancelbtn.cancel = 1
		self.cancelbtn.fillAfterRate = 1
	
def is_valid_cuboid(vertices):
    if len(vertices) != 8:
        return False
    x_values = set(vertex[0] for vertex in vertices)
    y_values = set(vertex[1] for vertex in vertices)
    z_values = set(vertex[2] for vertex in vertices)
    return len(x_values) == 2 and len(y_values) == 2 and len(z_values) == 2

def get_cuboid_dimensions(vertices):
    if not is_valid_cuboid(vertices):
        print("Error: The provided vertices do not form a valid cuboid.")
        return None
    x_coords = [vertex[0] for vertex in vertices]
    y_coords = [vertex[1] for vertex in vertices]
    z_coords = [vertex[2] for vertex in vertices]
    width = max(x_coords) - min(x_coords)
    height = max(y_coords) - min(y_coords)
    length = max(z_coords) - min(z_coords)
    return (round(width, 3), round(height, 3), round(length, 3))

def get_cuboid_center(vertices):
    if not is_valid_cuboid(vertices):
        print("Error: The provided vertices do not form a valid cuboid.")
        return None
    x_coords_sum = sum(vertex[0] for vertex in vertices)
    y_coords_sum = sum(vertex[1] for vertex in vertices)
    z_coords_sum = sum(vertex[2] for vertex in vertices)
    x_center = x_coords_sum / 8
    y_center = y_coords_sum / 8
    z_center = z_coords_sum / 8
    return (round(x_center, 3), round(y_center, 3), round(z_center, 3))

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
pattern = re.compile(r'"pos":\s\[\n\s+(-?\d+.?\d+?),\n\s+(-?\d+.?\d+?),\n\s+(-?\d+.?\d+?)\n\s+]')

def json_prettify(match):
  return f"\"pos\": [{match.group(1)}, {match.group(2)}, {match.group(3)}]"
json_formatted = pattern.sub(json_prettify, json.dumps(json_obj, indent=2))

cuboid_all= []
cuboid_current = []
modname = 0

dlg= ObjectDialog(MQWidget.getMainWindow())

if dlg.execute() == "ok":
	result = dlg.edit.text
	modname = dlg.modselectflag
	debug = dlg.checkbox1.checked

	for i in range(0, num):
		obj = doc.object[i]
		if obj is None:
			continue
		if obj.lock == 1:
			continue
		if obj.name == result:
			if debug == True:
				print(f"; Name: {obj.name} / Hitboxes: {int(obj.numFace/6+1)} / Faces: {obj.numFace} / Vertices: {obj.numVertex}")
			for j in range(0, obj.numVertex):
					x_pos = float("{:.3f}".format(obj.vertex[j].pos.x / 100))
					y_pos = float("{:.3f}".format(obj.vertex[j].pos.y / 100))
					z_pos = float("{:.3f}".format(obj.vertex[j].pos.z / 100))
					cuboid_current.append([x_pos, y_pos, z_pos])
					if (j+1)%8 == 0:
						cuboid_all.append(cuboid_current)
						cuboid_current = []
	
	for idx, cuboid in enumerate(cuboid_all):
		dimensions = get_cuboid_dimensions(cuboid) #assumes width is equal to length
		center = get_cuboid_center(cuboid)
		if modname == 1:
			if debug == True:
				print(idx+1, end = ': ')
			print(f"BoundingBox = {center[0]}, {center[1]}, {center[2]},  {dimensions[0]}, {dimensions[1]}")
		elif modname == 2:
			if debug == True:
				print(idx+1, end = ': ')
			print(f'{{width: {dimensions[0]}, "height": {dimensions[1]}, "x": {center[0]}, "y": {center[1]}, "z": {center[2]}}},')
		elif modname == 3:
			if debug == True:
				json_obj['collisionGroups'][0]['collisions'].append({
					"DEBUG_INDEX": idx+1,
					"pos": [center[0], center[1], center[2]],
					"width": dimensions[0],
					"height": dimensions[1]
				})
			else:
				json_obj['collisionGroups'][0]['collisions'].append({
					"pos": [center[0], center[1], center[2]],
					"width": dimensions[0],
					"height": dimensions[1]
				})
		else:
			MQSystem.println('Cannot resolve mod name!')

if modname == 3:
	print(pattern.sub(json_prettify, json.dumps(json_obj, indent=2)))
