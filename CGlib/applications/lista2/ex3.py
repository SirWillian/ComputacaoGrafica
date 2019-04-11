import sys
import glm
from math import *

args = sys.argv[1:]
print(args)

result=glm.mat4(1)

if(args[0]=='t'):
    #for i in range(3):
    #    result[i,3]=int(args[i+1])
    vec = glm.vec3(int(args[1]),int(args[2]),int(args[3]))
    result=glm.transpose(glm.translate(result,vec))

elif(args[0]=='s'):
    #for i in range(3):
    #    result[i,i]*=int(args[i+1])
    vec = glm.vec3(int(args[1]),int(args[2]),int(args[3]))
    result=glm.scale(result,vec)
    

elif(args[0]=='r'):
    #cols=[0,1,2]
    #cols.remove(ord(args[1])-120)
    #result[cols[0],cols[0]]=cos(radians(int(args[2])))
    #result[cols[1],cols[1]]=result[cols[0],cols[0]]
    #if(args[1]=='y'):
    #    result[cols[0],cols[1]]=sin(radians(int(args[2])))
    #    result[cols[1],cols[0]]=-sin(radians(int(args[2])))
    #else:
    #    result[cols[0],cols[1]]=-sin(radians(int(args[2])))
    #    result[cols[1],cols[0]]=sin(radians(int(args[2])))
    axis = glm.vec3()
    axis[ord(args[1])-120]=1
    result=glm.transpose(glm.rotate(result,glm.radians(float(args[2])),axis))
            
print(result)
