#import glm
#import numpy as np

class Vertex(object):
    def __init__(self,coordinates,index):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.z = coordinates[2]
        self.index = index
        #self.normal = glm.vec3(0,0,0)