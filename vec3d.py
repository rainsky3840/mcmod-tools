class Vector3D:
  # def __init__(self, x, y, z):
    # self.x = x
    # self.y = y
    # self.z = z

  def __init__(self, other):
    self.x = other[0]
    self.y = other[1]
    self.z = other[2]

  def __move__(self, other):
    if other.x != 0:
      self.x = self.x + other.x
    if other.y != 0:
      self.y = self.y + other.y
    if other.z != 0:
      self.z = self.z + other.z
    return f'{round(self.x, 4)}, {round(self.y, 4)}, {round(self.z, 4)}'
    # return Vector3D(self.x, self.y, self.z)
  
  def __scale__(self, other, scalar):
    self.x = self.x + (self.x - other.x) * (scalar - 1)
    self.y = self.y + (self.y - other.y) * (scalar - 1)
    self.z = self.z + (self.z - other.z) * (scalar - 1)
    return f'{round(self.x, 4)}, {round(self.y, 4)}, {round(self.z, 4)}'
    # return Vector3D(self.x, self.y, self.z)

  def __str__(self) -> str:
    return f'{round(self.x, 4)}, {round(self.y, 4)}, {round(self.z, 4)}'

# v1 = Vector3D([1.1, 2.2, 3.3])
# v2 = Vector3D([0, 0, 0])
# v3 = Vector3D([3, 4, 5])

# r1 = v1.__scale__(v2, 2)
# r2 = v1.__move__(v3)

# print(r1, type(r1))
# print(r2, type(r2))

# print(v1, type(v1))
# print(str(v1), type(str(v1)))