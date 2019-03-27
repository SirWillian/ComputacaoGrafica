import numpy as np
from math import acos, degrees

class Vec3(object):
    def __init__(self, x, y, z=0):
        self.coordinates=np.array([x,y,z])

    def __add__(self, vector):
        return Vec3(*(self.coordinates + vector.coordinates))

    def __sub__(self, vector):
        if(type(vector)!=Vec3):
            raise TypeError('Second operand must be of type Vec3')
        return Vec3(*(self.coordinates - vector.coordinates))

    def norm(self):
        return np.linalg.norm(self.coordinates)

    @staticmethod
    def dot(u,v):
        return np.dot(u.coordinates,v.coordinates)

    @staticmethod
    def cross(u,v):
        return Vec3(*np.cross(u.coordinates,v.coordinates))

    @staticmethod
    def angle_between(u,v,radians=False):
        angle = acos(Vec3.dot(u,v)/(u.norm()*v.norm()))
        return angle if radians else degrees(angle)

    @staticmethod
    def are_parallel(u,v):
        return Vec3.cross(u,v).norm()==0
