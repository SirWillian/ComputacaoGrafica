from Vertex import Vertex
from Triangle import Triangle
import numpy as np
from math import sqrt

class Mesh(object):
    def __init__(self, coordinates):
        self.triangles = []
        #self.normals = np.array([])
        coords = coordinates.ravel().reshape((coordinates.shape[0]*coordinates.shape[1],coordinates.shape[2]))
        vertices = np.array([Vertex(coords[i],i) for i in range(len(coords))]).reshape(coordinates.shape[0:2])
        vertex_normals = np.array([[np.array([0,0,0])] for i in vertices.size])
        for i in range(len(vertices)-1):
            for j in range(len(vertices[0])-1):
                tri1 = Triangle([vertices[i,j],vertices[i+1,j],vertices[i,j+1]])
                # Once for each vertex
                vertex_normals[i*len(vertices) + j] += tri1.normal
                vertex_normals[(i+1)*len(vertices) + j] += tri1.normal
                vertex_normals[i*len(vertices) + j + 1] += tri1.normal
                self.triangles.append(tri1)
                #self.normals = np.append(self.normals,[tri1.normal])

                tri2 = Triangle([vertices[i+1,j],vertices[i+1,j+1],vertices[i,j+1]])
                vertex_normals[(i+1)*len(vertices) + j] += tri2.normal
                vertex_normals[(i+1)*len(vertices) + j] += tri2.normal
                vertex_normals[i*len(vertices) + j + 1] += tri2.normal
                self.triangles.append(tri2)
                #self.normals = np.append(self.normals,[tri2.normal])

        for i in range(len())
        self.triangles = np.array(self.triangles)

    def getVertexIndices(self):
        return np.array([v.index for tri in self.triangles for v in tri.vertices],dtype=np.uint32)

    def getTriangleNormalArrows(self):
        arrowLength = 1/(sqrt(len(self.triangles)))
        print(arrowLength)
        return np.array([[tri.getCentroid(), tri.getCentroid()+arrowLength*tri.normal] for tri in self.triangles],dtype=np.float32).ravel()
