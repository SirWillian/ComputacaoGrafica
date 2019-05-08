import cv2
import numpy as np

class Terrain(object):
    def __init__(self, path):
        img = cv2.imread(path,0)
        if(img is not None):
            self.width = img.shape[0]
            self.length = img.shape[1]
            self.height = np.max(img)
            # Center terrain in 0,0
            self.vertices = np.array([[(i-img.shape[0]/2)/img.shape[0],img[i,j]/255,(j-img.shape[1]/2)/img.shape[1]]
                                     for i in range(img.shape[0])
                                     for j in range(img.shape[1])], dtype=np.float32)
    
