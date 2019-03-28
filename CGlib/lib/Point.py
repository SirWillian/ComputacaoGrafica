import numpy as np
from Vec3 import Vec3

class Point(object):
    def __init__(self, x, y, z=0):
        self.coordinates=np.array([x,y,z], dtype=np.float32)

    def __add__(self, vec3):
        if(type(vec3)!=Vec3):
            raise TypeError('Second operand must be of type Vec3')
        return Point(*(self.coordinates + vec3.coordinates))

    def __sub__(self, point):
        if(type(point)!=Point):
            raise TypeError('Second operand must be of type Point')
        return Vec3(*(self.coordinates - point.coordinates))
