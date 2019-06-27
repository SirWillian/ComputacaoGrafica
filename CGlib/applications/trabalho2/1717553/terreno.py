#!/usr/bin/env python3
import sys

import numpy as np
from OpenGL.arrays import ArrayDatatype
from OpenGL.GL import *
from OpenGL.GLUT import *

import glm
from ShaderProgram import ShaderProgram
from Terrain import Terrain

# OpenGL
VAO = VBO = CBO = EBO = 0
program_id = 0
vertex_shader = open("simple3.vert").read()
fragment_shader = open("simple3.frag").read()

# Terrain
terrain=0
indices=[]

# Model-View-Projection
rotation_matrix = glm.mat4(1)
scale_matrix = glm.mat4(1)
scale_vector = glm.vec3(1,1,1)
view_origin = glm.vec3(0,0,0.7)
view_matrix = glm.lookAt(view_origin, view_origin+glm.vec3(0,0,-1), glm.vec3(0,1,0))
perspective_matrix = glm.perspective(glm.radians(90), 16/9, 0.1, 100)

# Keyboard control
MESH_FLAG = 8
SCALE_FLAG = 4
ROTATION_FLAG = 2
TRANSLATION_FLAG = 1
TRANSLATION_STEP = 0.05
ROTATION_STEP = glm.radians(9)
SCALE_STEP = 0.1
key_flags = 8

def Keyboard(key, x, y):
    global view_origin, view_matrix, rotation_matrix, scale_vector, scale_matrix, key_flags

    if(key==27 or key == b'q' or key == b'Q'):
        sys.exit(0)
        
    elif(key==b't'):
        key_flags &= 8+TRANSLATION_FLAG
        key_flags ^= TRANSLATION_FLAG    
    elif(key==b'r'):
        key_flags &= 8+ROTATION_FLAG
        key_flags ^= ROTATION_FLAG    
    elif(key==b'e'):
        key_flags &= 8+SCALE_FLAG
        key_flags ^= SCALE_FLAG
    elif(key==b'v'):
        key_flags ^= MESH_FLAG

    if(key_flags & TRANSLATION_FLAG == TRANSLATION_FLAG):
        if(key==b'a'):
            view_origin[2]-=TRANSLATION_STEP
        elif(key==b'd'):
            view_origin[2]+=TRANSLATION_STEP
        view_matrix = glm.lookAt(view_origin, view_origin+glm.vec3(0,0,-1), glm.vec3(0,1,0))

    elif(key_flags & ROTATION_FLAG == ROTATION_FLAG):
        if(key==b'a'):
            rotation_matrix = glm.rotate(rotation_matrix, ROTATION_STEP, [0,0,1])
        elif(key==b'd'):
            rotation_matrix = glm.rotate(rotation_matrix, -ROTATION_STEP, [0,0,1])

    elif(key_flags & SCALE_FLAG == SCALE_FLAG):
        if(key==b'a'):
            scale_vector[2]+=SCALE_STEP
        elif(key==b'd'):
            scale_vector[2]-=SCALE_STEP
        scale_matrix = glm.scale(glm.mat4(1), scale_vector)
        
    glutPostRedisplay()

def Special(key, x, y):
    global view_origin, view_matrix, scale_matrix, rotation_matrix
    if(key_flags & TRANSLATION_FLAG == TRANSLATION_FLAG):
        if(key==GLUT_KEY_LEFT):
            view_origin[0]+=TRANSLATION_STEP
        elif(key==GLUT_KEY_RIGHT):
            view_origin[0]-=TRANSLATION_STEP
        elif(key==GLUT_KEY_UP):
            view_origin[1]-=TRANSLATION_STEP
        elif(key==GLUT_KEY_DOWN):
            view_origin[1]+=TRANSLATION_STEP
        view_matrix = glm.lookAt(view_origin, view_origin+glm.vec3(0,0,-1), glm.vec3(0,1,0))

    elif(key_flags & ROTATION_FLAG == ROTATION_FLAG):
        if(key==GLUT_KEY_LEFT):
            rotation_matrix = glm.rotate(rotation_matrix, -ROTATION_STEP, [0,1,0])
        elif(key==GLUT_KEY_RIGHT):
            rotation_matrix = glm.rotate(rotation_matrix, ROTATION_STEP, [0,1,0])
        elif(key==GLUT_KEY_UP):
            rotation_matrix = glm.rotate(rotation_matrix, ROTATION_STEP, [1,0,0])
        elif(key==GLUT_KEY_DOWN):
            rotation_matrix = glm.rotate(rotation_matrix, -ROTATION_STEP, [1,0,0])
    
    elif(key_flags & SCALE_FLAG == SCALE_FLAG):
        if(key==GLUT_KEY_LEFT):
            scale_vector[0]-=SCALE_STEP
        elif(key==GLUT_KEY_RIGHT):
            scale_vector[0]+=SCALE_STEP
        elif(key==GLUT_KEY_UP):
            scale_vector[1]+=SCALE_STEP
        elif(key==GLUT_KEY_DOWN):
            scale_vector[1]-=SCALE_STEP
        scale_matrix = glm.scale(glm.mat4(1), scale_vector)
        
    glutPostRedisplay()

def Init():
    global VAO, VBO, terrain, perspective_matrix, view_matrix, view_origin, indices
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    terrain = Terrain(sys.argv[1])
    vertices = terrain.vertices

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(vertices), vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)
    
    colors = vertices+0.3

    CBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, CBO)
    glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(colors), colors, GL_STATIC_DRAW)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(1)

    #indices=[]
    #for i in range(terrain.width-1):
    #    for j in range(terrain.length-1):
    #        indices.append(i*terrain.length+j)
    #        indices.append(i*terrain.length+j+1)
    #        indices.append((i+1)*terrain.length+j)

    #        indices.append((i+1)*terrain.length+j)
    #        indices.append((i+1)*terrain.length+j+1)
    #        indices.append(i*terrain.length+j+1)
    #indices = np.array(indices, dtype=np.uint32)

    indices = terrain.mesh.getVertexIndices()

    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(indices), indices, GL_STATIC_DRAW)

    
    
    global program_id
    program = ShaderProgram(vertex_shader, fragment_shader)
    program_id = program.program_id
    glUseProgram(program_id)
            
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glPointSize(1.4)
    glClearColor(0.1,0.1,0.1,1)


def Display():
    global perspective_matrix, program_id, terrain

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    transform = perspective_matrix * view_matrix * rotation_matrix * scale_matrix

    transformLoc = glGetUniformLocation(program_id, "transform")
    glUniformMatrix4fv(transformLoc, 1, GL_FALSE, glm.value_ptr(transform))

    glBindVertexArray(VAO)
    if (key_flags & MESH_FLAG == MESH_FLAG):
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
    else:
        glDrawArrays(GL_POINTS, 0, terrain.vertices.size//3)
    
    glutSwapBuffers()


if __name__ == "__main__":
    if(len(sys.argv)<2):
        print("Usage: ./terreno.py <path to image>")
        sys.exit(0)
    
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(1366, 768)
    glutInitContextVersion(3, 3)
    glutInitContextProfile(GLUT_CORE_PROFILE)
    glutCreateWindow(bytes(sys.argv[0], 'utf-8'))

    Init()
    glutKeyboardFunc(Keyboard)
    glutSpecialFunc(Special)
    glutDisplayFunc(Display)

    glutMainLoop()
