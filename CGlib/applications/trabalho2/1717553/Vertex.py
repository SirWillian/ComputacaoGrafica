import numpy as np

class Vertex(object):
    def __init__(self,coordinates,index):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.z = coordinates[2]
        self.index = index
        self.normal = np.array([0,0,0], dtype=np.float32)

    def getCoordinates(self):
        return np.array([self.x,self.y,self.z], dtype=np.float32)