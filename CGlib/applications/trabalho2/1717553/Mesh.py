from Vertex import Vertex
from Triangle import Triangle
import numpy as np

class Mesh(object):
    def __init__(self, coordinates):
        self.triangles = []
        coords = coordinates.ravel().reshape((coordinates.shape[0]*coordinates.shape[1],coordinates.shape[2]))
        vertices = np.array([Vertex(coords[i],i) for i in range(len(coords))]).reshape(coordinates.shape[0:2])
        for i in range(len(vertices)-1):
            for j in range(len(vertices[0])-1):
                self.triangles.append(Triangle([vertices[i,j],vertices[i+1,j],vertices[i,j+1]]))
                self.triangles.append(Triangle([vertices[i+1,j],vertices[i+1,j+1],vertices[i,j+1]]))
        self.triangles = np.array(self.triangles)

    def getVertexIndices(self):
        return np.array([v.index for tri in self.triangles for v in tri.vertices],dtype=np.uint32)