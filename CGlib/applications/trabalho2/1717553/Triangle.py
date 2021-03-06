import glm
import numpy as np

class Triangle(object):
    def __init__(self,vertices):
        self.vertices=vertices
        # For P, Q, R, defined counter-clockwise, glm.cross(R-Q, P-Q)
        PQ = glm.vec3(vertices[0].x-vertices[1].x,vertices[0].y-vertices[1].y,vertices[0].z-vertices[1].z)
        RQ = glm.vec3(vertices[2].x-vertices[1].x,vertices[2].y-vertices[1].y,vertices[2].z-vertices[1].z)
        normal = glm.normalize(glm.cross(RQ,PQ))
        self.normal = np.array([normal.x,normal.y,normal.z], dtype=np.float32)

    def getCentroid(self):
        return np.array([self.vertices[0].x + self.vertices[1].x + self.vertices[2].x,
                         self.vertices[0].y + self.vertices[1].y + self.vertices[2].y,
                         self.vertices[0].z + self.vertices[1].z + self.vertices[2].z])/3
