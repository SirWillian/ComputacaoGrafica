import numpy as np

class Point(object):
    def __init__(self, x, y, z=0):
        self.coordinates=np.array([x,y,z])
