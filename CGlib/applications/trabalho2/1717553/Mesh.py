from Vertex import Vertex
from Triangle import Triangle
import numpy as np
from math import sqrt
import glm

class Mesh(object):
    def __init__(self, coordinates):
        self.triangles = []
        #self.normals = np.array([])
        coords = coordinates.ravel().reshape((coordinates.shape[0]*coordinates.shape[1],coordinates.shape[2]))
        vertices = np.array([Vertex(coords[i],i) for i in range(len(coords))]).reshape(coordinates.shape[0:2])
        vertex_normals = np.array([np.array([0,0,0], dtype=np.float32) for i in range(vertices.size)]).reshape(coordinates.shape)
        #print(vertices.shape)

        width = len(vertices)
        height = len(vertices[0])
        for i in range(width-1):
            for j in range(height-1):
                tri1 = Triangle([vertices[i,j],vertices[i+1,j],vertices[i,j+1]])
                # Once for each vertex
                vertex_normals[i,j] += tri1.normal
                vertex_normals[i+1,j] += tri1.normal
                vertex_normals[i,j+1] += tri1.normal
                self.triangles.append(tri1)
                #self.normals = np.append(self.normals,[tri1.normal])

                tri2 = Triangle([vertices[i+1,j],vertices[i+1,j+1],vertices[i,j+1]])
                vertex_normals[i+1,j] += tri2.normal
                vertex_normals[i+1,j+1] += tri2.normal
                vertex_normals[i,j+1] += tri2.normal
                self.triangles.append(tri2)
                #self.normals = np.append(self.normals,[tri2.normal])
        for i in range(width):
            for j in range(height):
                normal = glm.normalize(vertex_normals[i,j])
                vertices[i,j].normal = np.array([normal.x,normal.y,normal.z])
        self.triangles = np.array(self.triangles)

    def getVertexIndices(self):
        return np.array([v.index for tri in self.triangles for v in tri.vertices],dtype=np.uint32)

    def getTriangleNormalArrows(self):
        arrowLength = 1/(sqrt(len(self.triangles)))
        #print(arrowLength)
        return np.array([[tri.getCentroid(), tri.getCentroid()+arrowLength*tri.normal] for tri in self.triangles],dtype=np.float32).ravel()
    
    def getVertexNormalArrows(self):
        arrowLength = 1/(sqrt(len(self.triangles)))
        return np.array([[v.getCoordinates(), v.getCoordinates()+arrowLength*v.normal] \
                        for tri in self.triangles for v in tri.vertices], dtype=np.float32).ravel()

    def getTriangleVertices(self):
        return np.array([v.getCoordinates() for tri in self.triangles for v in tri.vertices], dtype=np.float32)

    def getTriangleNormals(self):
        return np.array([[tri.normal]*3 for tri in self.triangles], dtype=np.float32)

    def getVertexNormals(self):
        # All vertices, without repetition, sorted by index
        vertices = sorted(list(dict.fromkeys([v for tri in self.triangles for v in tri.vertices])), key=lambda v: v.index)
        return np.array([v.normal for v in vertices], dtype=np.float32)