import cv2
import numpy as np
from Mesh import Mesh

class Terrain(object):
    def __init__(self, path):
        img = cv2.imread(path,cv2.IMREAD_UNCHANGED)
        if(img is not None):
            self.width = img.shape[0]
            self.length = img.shape[1]
            self.height = np.max(img)
            # Center terrain in 0,0,0 and normalize y
            img_min = np.min(img)
            img_max = np.max(img)
            self.vertices = np.array([[(img.shape[0]/2-i)/img.shape[0],((img[i,j]-img_min)/(img_max-img_min))-0.5,(j-img.shape[1]/2)/img.shape[1]]
                                     for i in range(img.shape[0])
                                     for j in range(img.shape[1])], dtype=np.float32).reshape((img.shape[0],img.shape[1],3))
            self.mesh = Mesh(self.vertices)
    
