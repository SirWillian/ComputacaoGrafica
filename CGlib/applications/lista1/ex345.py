import numpy as np
import sys
sys.path.append('../../lib')

from Vec3 import Vec3
from Point import Point


print("3)")
u = Vec3(1,1,0)
v = Vec3(0,2,3)
w = Vec3(2,4,3)

#Implementar conversão de base
print("u = 0.5w - 0.5v")
print("v = w - 2u")
print("w = 2u + v")

print("Angulo entre u v: "+str(Vec3.angle_between(u,v))+
      " u x v: "+str(Vec3.cross(u,v).coordinates))
print("Angulo entre u w: "+str(Vec3.angle_between(u,w))+
      " u x w: "+str(Vec3.cross(u,w).coordinates))
print("Angulo entre v w: "+str(Vec3.angle_between(v,w))+
      " v x w: "+str(Vec3.cross(v,w).coordinates))

print("\n4)")
u = Vec3(-2,3,1)
v = Vec3(0,4,1)
print("Area do paralelogramo: "+str(Vec3.cross(u,v).norm()))

print("\n5)")
u = Vec3(2,6,12)
v = Vec3(1,3,6)
print("u e v são paralelos? "+str(Vec3.are_parallel(u,v)))
