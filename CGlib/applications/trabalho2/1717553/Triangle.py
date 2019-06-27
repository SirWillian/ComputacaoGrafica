import glm

class Triangle(object):
    def __init__(self,vertices):
        self.vertices=vertices
        # For P, Q, R, defined counter-clockwise, glm.cross(R-Q, P-Q)
        RQ = glm.vec3(vertices[0].x-vertices[1].x,vertices[0].y-vertices[1].y,vertices[0].z-vertices[1].z)
        PQ = glm.vec3(vertices[2].x-vertices[1].x,vertices[2].y-vertices[1].y,vertices[2].z-vertices[1].z)
        normal = glm.normalize(glm.cross(RQ,PQ))*0.1
        self.normal = [normal.x,normal.y,normal.z]
