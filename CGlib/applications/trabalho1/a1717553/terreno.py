#!/usr/bin/env python3
import numpy as np
from OpenGL.arrays import ArrayDatatype
from OpenGL.GL import *
from OpenGL.GLUT import *
import glm
import sys
from math import cos, sin, pi
from ShaderProgram import ShaderProgram
from Terrain import Terrain


# Globals
VAO = VBO = CBO = EBO = 0
program_id = 0
vertex_shader = open("simple3.vert").read()
fragment_shader = open("simple3.frag").read()


terrain=0
indices=[]

view_origin = glm.vec3(0,0,0)
view_matrix = glm.mat4(1)
perspective_matrix = glm.mat4(1)

def Keyboard(key, x, y):
    global view_origin, view_matrix

    print_matrix = False
    
    if(key==27 or key == b'q' or key == b'Q'):
        sys.exit(0)
    elif(key==b'd'):
        print("Dimétrica:")
        view_origin=glm.vec3(1,1,1)
        print_matrix = True
    elif(key==b't'):
        print("Trimétrica:")
        view_origin=glm.vec3(1,0.8,0.5)
        print_matrix = True
    elif(key==b'i'):
        print("Isométrica:")
        view_origin=glm.vec3(1,1.5,1)
        print_matrix = True
    
    view_matrix = glm.lookAt(view_origin, glm.vec3(0,0,0), glm.vec3(0,1,0))
    if(print_matrix):
        print(view_matrix)
    glutPostRedisplay()
        

def Init():
    global VAO, VBO, terrain, perspective_matrix, view_matrix, view_origin, indices
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    terrain = Terrain(sys.argv[1])
    vertices = terrain.vertices

    #print(vertices)

    view_origin = glm.vec3(1,1,1)
    #view_origin = glm.vec3(0,terrain.height/2,terrain.width/2)
    view_matrix = glm.lookAt(view_origin, glm.vec3(0,0,0), glm.vec3(0,1,0))
    #perspective_matrix = glm.ortho(-terrain.length/2, terrain.length/2,
    #                               -terrain.height/2, terrain.height/2,
    #                               0, terrain.width)
    #perspective_matrix = glm.ortho(-1,1,-1,1,0,100)
    #perspective_matrix = glm.ortho(-3,3,0,255,-3,3)
    perspective_matrix = glm.perspective(glm.radians(90), 1, 0.1, 100)

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(vertices), vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)
    
    CBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, CBO)
    glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(vertices), vertices/np.max(vertices), GL_STATIC_DRAW)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(1)

    indices=[]
    for i in range(terrain.width-1):
        for j in range(terrain.length-1):
            indices.append(i*terrain.width+j)
            indices.append(i*terrain.width+j+1)
            indices.append((i+1)*terrain.width+j)

            indices.append((i+1)*terrain.width+j)
            indices.append((i+1)*terrain.width+j+1)
            indices.append(i*terrain.width+j+1)
    indices = np.array(indices, dtype=np.uint32)
    print(indices)

    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(indices), indices, GL_STATIC_DRAW)

    
    
    global program_id
    program = ShaderProgram(vertex_shader, fragment_shader)
    program_id = program.program_id
    glUseProgram(program_id)
            
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    #glPointSize(1)


def Display():
    global perspective_matrix, program_id, terrain

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    transform = perspective_matrix * view_matrix

    transformLoc = glGetUniformLocation(program_id, "transform")
    glUniformMatrix4fv(transformLoc, 1, GL_FALSE, glm.value_ptr(transform))

    glBindVertexArray(VAO)
    #glDrawArrays(GL_POINTS, 0, terrain.vertices.size//3);
    #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
    
    glutSwapBuffers()


if __name__ == "__main__":
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(512, 512)
    glutInitContextVersion(3, 3)
    glutInitContextProfile(GLUT_CORE_PROFILE)
    glutCreateWindow(bytes(sys.argv[0], 'utf-8'))

    Init()
    glutKeyboardFunc(Keyboard)
    glutDisplayFunc(Display)

    glutMainLoop()
