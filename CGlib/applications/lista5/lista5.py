#!/usr/bin/env python3
import numpy as np
from OpenGL.arrays import ArrayDatatype
from OpenGL.GL import *
from OpenGL.GLUT import *
import glm
import sys
from math import cos, sin, pi
from ShaderProgram import ShaderProgram


# Globals
VAO = VBO = CBO = 0
program_id = 0
vertex_shader = open("simple3.vert").read()
fragment_shader = open("simple3.frag").read()

view_origin = glm.vec3(1,1,1)
yaw = pi/2
pitch = pi/2
view_matrix = glm.lookAt(view_origin, glm.vec3(0,0,0), glm.vec3(0,1,0))
#view_matrix = glm.mat4(1)
perspective_matrix = glm.ortho(-1, 1, -1, 1, 0, 100)
#perspective_matrix = glm.mat4(1)

def Keyboard(key, x, y):
    global view_origin, view_matrix

    print_matrix = False
    
    if(key==27 or key == b'q' or key == b'Q'):
        sys.exit(0)
    elif(key==b'd'):
        print("Dimétrica:")
        view_origin=glm.vec3(1,1,0.5)
        print_matrix = True
    elif(key==b't'):
        print("Trimétrica:")
        view_origin=glm.vec3(1,0.3,0.5)
        print_matrix = True
    elif(key==b'i'):
        print("Isométrica:")
        view_origin=glm.vec3(1,1,1)
        print_matrix = True
    
    view_matrix = glm.lookAt(view_origin, glm.vec3(0,0,0), glm.vec3(0,1,0))
    if(print_matrix):
        print(view_matrix)
    glutPostRedisplay()
        

def Init():
    global VAO, VBO, CBO
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    vertices = np.array([
        -0.5,-0.5,-0.5, 1.0,
        -0.5,-0.5, 0.5, 1.0,
        -0.5, 0.5, 0.5, 1.0,
         0.5, 0.5,-0.5, 1.0,
        -0.5,-0.5,-0.5, 1.0,
        -0.5, 0.5,-0.5, 1.0,
         0.5,-0.5, 0.5, 1.0,
        -0.5,-0.5,-0.5, 1.0,
         0.5,-0.5,-0.5, 1.0,
         0.5, 0.5,-0.5, 1.0,
         0.5,-0.5,-0.5, 1.0,
        -0.5,-0.5,-0.5, 1.0,
        -0.5,-0.5,-0.5, 1.0,
        -0.5, 0.5, 0.5, 1.0,
        -0.5, 0.5,-0.5, 1.0,
         0.5,-0.5, 0.5, 1.0,
        -0.5,-0.5, 0.5, 1.0,
        -0.5,-0.5,-0.5, 1.0,
        -0.5, 0.5, 0.5, 1.0,
        -0.5,-0.5, 0.5, 1.0,
         0.5,-0.5, 0.5, 1.0,
         0.5, 0.5, 0.5, 1.0,
         0.5,-0.5,-0.5, 1.0,
         0.5, 0.5,-0.5, 1.0,
         0.5,-0.5,-0.5, 1.0,
         0.5, 0.5, 0.5, 1.0,
         0.5,-0.5, 0.5, 1.0,
         0.5, 0.5, 0.5, 1.0,
         0.5, 0.5,-0.5, 1.0,
        -0.5, 0.5,-0.5, 1.0,
         0.5, 0.5, 0.5, 1.0,
        -0.5, 0.5,-0.5, 1.0,
        -0.5, 0.5, 0.5, 1.0,
         0.5, 0.5, 0.5, 1.0,
        -0.5, 0.5, 0.5, 1.0,
         0.5,-0.5, 0.5, 1.0
    ], dtype=np.float32)

    vertices = np.array([
        -0.5,-0.5,-0.5, 1.0,
        -0.5,-0.5, 0.5, 1.0,
        -0.5, 0.5, 0.5, 1.0,
         0.5, 0.5,-0.5, 1.0,
        -0.5,-0.5,-0.5, 1.0,
        -0.5, 0.5,-0.5, 1.0,
         0.5,-0.5, 0.5, 1.0,
        -0.5,-0.5,-0.5, 1.0,
         0.5,-0.5,-0.5, 1.0,
         0.5, 0.5,-0.5, 1.0,
         0.5,-0.5,-0.5, 1.0,
        -0.5,-0.5,-0.5, 1.0,
        -0.5,-0.5,-0.5, 1.0,
        -0.5, 0.5, 0.5, 1.0,
        -0.5, 0.5,-0.5, 1.0,
         0.5,-0.5, 0.5, 1.0,
        -0.5,-0.5, 0.5, 1.0,
        -0.5,-0.5,-0.5, 1.0,
        -0.5, 0.5, 0.5, 1.0,
        -0.5,-0.5, 0.5, 1.0,
         0.5,-0.5, 0.5, 1.0,
         0.5, 0.5, 0.5, 1.0,
         0.5,-0.5,-0.5, 1.0,
         0.5, 0.5,-0.5, 1.0,
         0.5,-0.5,-0.5, 1.0,
         0.5, 0.5, 0.5, 1.0,
         0.5,-0.5, 0.5, 1.0,
         0.5, 0.5, 0.5, 1.0,
         0.5, 0.5,-0.5, 1.0,
        -0.5, 0.5,-0.5, 1.0,
         0.5, 0.5, 0.5, 1.0,
        -0.5, 0.5,-0.5, 1.0,
        -0.5, 0.5, 0.5, 1.0,
         0.5, 0.5, 0.5, 1.0,
        -0.5, 0.5, 0.5, 1.0,
         0.5,-0.5, 0.5, 1.0
    ], dtype=np.float32)

    colors = np.array([
        0.014, 0.184, 0.576, 1.0,#
        0.014, 0.184, 0.576, 1.0,#
        0.014, 0.184, 0.576, 1.0,#
        0.483, 0.596, 0.789, 1.0,#
        0.483, 0.596, 0.789, 1.0,#
        0.483, 0.596, 0.789, 1.0,#
        0.676, 0.977, 0.133, 1.0,#
        0.676, 0.977, 0.133, 1.0,#
        0.676, 0.977, 0.133, 1.0,#
        0.483, 0.596, 0.789, 1.0,#
        0.483, 0.596, 0.789, 1.0,#
        0.483, 0.596, 0.789, 1.0,#
        0.014, 0.184, 0.576, 1.0,#
        0.014, 0.184, 0.576, 1.0,#
        0.014, 0.184, 0.576, 1.0,#
        0.676, 0.977, 0.133, 1.0,#
        0.676, 0.977, 0.133, 1.0,#
        0.676, 0.977, 0.133, 1.0,#
        0.673, 0.211, 0.457, 1.0,#
        0.673, 0.211, 0.457, 1.0,#
        0.673, 0.211, 0.457, 1.0,#
        0.055, 0.953, 0.042, 1.0,#
        0.055, 0.953, 0.042, 1.0,#
        0.055, 0.953, 0.042, 1.0,#
        0.055, 0.953, 0.042, 1.0,#
        0.055, 0.953, 0.042, 1.0,#
        0.055, 0.953, 0.042, 1.0,#
        0.997, 0.513, 0.064, 1.0,#
        0.997, 0.513, 0.064, 1.0,#
        0.997, 0.513, 0.064, 1.0,#
        0.997, 0.513, 0.064, 1.0,#
        0.997, 0.513, 0.064, 1.0,#
        0.997, 0.513, 0.064, 1.0,#
        0.673, 0.211, 0.457, 1.0,#
        0.673, 0.211, 0.457, 1.0,#
        0.673, 0.211, 0.457, 1.0#
    ], dtype=np.float32)

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(vertices), vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)
    
    CBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, CBO)
    glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(colors), colors, GL_STATIC_DRAW)
    glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(1)
    
    global program_id
    program = ShaderProgram(vertex_shader, fragment_shader)
    program_id = program.program_id
    glUseProgram(program_id)
            
    glEnable(GL_DEPTH_TEST)


def Display():
    global perspective_matrix, view_matrix, program_id

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    transform = perspective_matrix * view_matrix

    transformLoc = glGetUniformLocation(program_id, "transform")
    glUniformMatrix4fv(transformLoc, 1, GL_FALSE, glm.value_ptr(transform))

    glBindVertexArray(VAO)
    glDrawArrays(GL_TRIANGLES, 0, 12*3);
    
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
