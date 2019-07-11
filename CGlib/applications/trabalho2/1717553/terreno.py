#!/usr/bin/env python3
import sys

import numpy as np
from OpenGL.arrays import ArrayDatatype
from OpenGL.GL import *
from OpenGL.GLUT import *

import glm
from math import cos, sin, pi
from ShaderProgram import ShaderProgram
from Terrain import Terrain

# OpenGL
meshVAO = arrowsVAO = VBO = CBO = EBO = 0
program_id = 0

# Terrain
terrain=0
indices=[]
normals=[]
colors=[]
normal_arrows=[]

# Model-View-Projection
rotation_matrix = glm.mat4(1)
scale_matrix = glm.mat4(1)
scale_vector = glm.vec3(1,1,1)
view_origin = glm.vec3(0,0,0.7)
view_matrix = glm.lookAt(view_origin, view_origin+glm.vec3(0,0,-1), glm.vec3(0,1,0))
perspective_matrix = glm.perspective(glm.radians(90), 16/9, 0.1, 100)

# Lighting
lightRadius = 1
lightAngle = pi/2
lightHeight = 1
lightPos = glm.vec3(lightRadius*cos(lightAngle),lightHeight,lightRadius*sin(lightAngle))
lightColor = glm.vec3(1,1,1)

# System flags
NORMAL_COLORS_FLAG = 128
LIGHTING_FLAG = 64
GOURAUD_FLAG = 32
NORMAL_ARROW_FLAG = 16
POINTS_FLAG = 8
SCALE_FLAG = 4
ROTATION_FLAG = 2
TRANSLATION_FLAG = 1
key_flags = 0

# Keyboard control constants
TRANSLATION_STEP = 0.05
ROTATION_STEP = glm.radians(9)
SCALE_STEP = 0.1

def Keyboard(key, x, y):
    global view_origin, view_matrix, rotation_matrix, scale_vector, scale_matrix, key_flags, lightAngle, lightHeight, lightPos

    untouched_flags = POINTS_FLAG + NORMAL_ARROW_FLAG + GOURAUD_FLAG + LIGHTING_FLAG + NORMAL_COLORS_FLAG

    if(key==27 or key == b'q' or key == b'Q'):
        sys.exit(0)

    elif(key==b't'):
        key_flags &= untouched_flags+TRANSLATION_FLAG
        key_flags ^= TRANSLATION_FLAG
    elif(key==b'r'):
        key_flags &= untouched_flags+ROTATION_FLAG
        key_flags ^= ROTATION_FLAG
    elif(key==b'e'):
        key_flags &= untouched_flags+SCALE_FLAG
        key_flags ^= SCALE_FLAG

    elif(key==b'c' and key_flags & LIGHTING_FLAG == LIGHTING_FLAG):
        key_flags ^= NORMAL_COLORS_FLAG
        glBindBuffer(GL_ARRAY_BUFFER, CBO)
        if (key_flags & NORMAL_COLORS_FLAG == NORMAL_COLORS_FLAG):
            glBufferSubData(GL_ARRAY_BUFFER, 0, ArrayDatatype.arrayByteCount(normals), normals)
        else:
            glBufferSubData(GL_ARRAY_BUFFER, 0, ArrayDatatype.arrayByteCount(colors), colors)
    
    elif(key==b'j'):
        lightAngle+=0.0525
    elif(key==b'l'):
        lightAngle-=0.0525
    elif(key==b'i'):
        lightHeight+=0.1
    elif(key==b'k'):
        lightHeight-=0.1
    lightPos = glm.vec3(lightRadius*cos(lightAngle),lightHeight,lightRadius*sin(lightAngle))

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

def SetSystemFlags(mode):
    global key_flags
    if (mode=='1'):
        key_flags = POINTS_FLAG
    elif (mode=='3'):
        key_flags = NORMAL_ARROW_FLAG
    elif (mode=='4'):
        key_flags = NORMAL_ARROW_FLAG + GOURAUD_FLAG
    elif (mode=='5'):
        key_flags = LIGHTING_FLAG
    elif (mode=='6'):
        key_flags = LIGHTING_FLAG + GOURAUD_FLAG

def Init():
    global meshVAO, arrowsVAO, VBO, CBO, terrain, indices, normals, colors, normal_arrows

    SetSystemFlags(sys.argv[2])

    meshVAO = glGenVertexArrays(1)
    glBindVertexArray(meshVAO)

    terrain = Terrain(sys.argv[1])
    if (key_flags == LIGHTING_FLAG):
        vertices = terrain.mesh.getTriangleVertices()
    else:
        vertices = terrain.vertices
    
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(vertices), vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)

    if (key_flags & GOURAUD_FLAG == GOURAUD_FLAG):
        normals = terrain.mesh.getVertexNormals()
    else:
        normals = terrain.mesh.getTriangleNormals()
    if (key_flags & LIGHTING_FLAG == LIGHTING_FLAG):
        NBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, NBO)
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(normals), normals, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(1)

    colors = vertices+0.3

    CBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, CBO)
    glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(colors), None, GL_STATIC_DRAW)
    glBufferSubData(GL_ARRAY_BUFFER, 0, ArrayDatatype.arrayByteCount(colors), colors)
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(2)

    indices = terrain.mesh.getVertexIndices()

    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(indices), indices, GL_STATIC_DRAW)

    if (key_flags & NORMAL_ARROW_FLAG == NORMAL_ARROW_FLAG):
        arrowsVAO = glGenVertexArrays(1)
        glBindVertexArray(arrowsVAO)

        if (key_flags & GOURAUD_FLAG == GOURAUD_FLAG):
            normal_arrows = terrain.mesh.getVertexNormalArrows()
        else:
            normal_arrows = terrain.mesh.getTriangleNormalArrows()

        arrow_NBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, arrow_NBO)
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(normal_arrows), normal_arrows, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)

        arrow_CBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, arrow_CBO)
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(normal_arrows), np.ones(normal_arrows.size,dtype=np.float32), GL_STATIC_DRAW)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(2)

    global program_id
    vertex_shader = fragment_shader = 0
    if (key_flags & LIGHTING_FLAG == LIGHTING_FLAG):
        vertex_shader = open("shading.vert").read()
        fragment_shader = open("shading.frag").read()
    else:
        vertex_shader = open("simple3.vert").read()
        fragment_shader = open("simple3.frag").read()
    
    program = ShaderProgram(vertex_shader, fragment_shader)
    program_id = program.program_id
    glUseProgram(program_id)

    if (key_flags & POINTS_FLAG == POINTS_FLAG):
        glPolygonMode(GL_FRONT_AND_BACK, GL_POINT)
    elif (key_flags & LIGHTING_FLAG == 0):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glPointSize(1.4)
    glClearColor(0.1,0.1,0.1,1)
    glEnable(GL_DEPTH_TEST)


def Display():
    global program_id, terrain

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Load shader uniforms
    if (key_flags & LIGHTING_FLAG == 0):
        transform = perspective_matrix * view_matrix * rotation_matrix * scale_matrix
        transformLoc = glGetUniformLocation(program_id, "transform")
        glUniformMatrix4fv(transformLoc, 1, GL_FALSE, glm.value_ptr(transform))
    else:
        object_transform = rotation_matrix * scale_matrix

        modelLoc = glGetUniformLocation(program_id, "model")
        glUniformMatrix4fv(modelLoc, 1, GL_FALSE, glm.value_ptr(object_transform))
        viewLoc = glGetUniformLocation(program_id, "view")
        glUniformMatrix4fv(viewLoc, 1, GL_FALSE, glm.value_ptr(view_matrix))
        projectionLoc = glGetUniformLocation(program_id, "projection")
        glUniformMatrix4fv(projectionLoc, 1, GL_FALSE, glm.value_ptr(perspective_matrix))

        lightColorLoc = glGetUniformLocation(program_id, "lightColor")
        glUniform3fv(lightColorLoc, 1, glm.value_ptr(lightColor))
        lightPosLoc = glGetUniformLocation(program_id, "lightPos")
        glUniform3fv(lightPosLoc, 1, glm.value_ptr(lightPos))
        viewPosLoc = glGetUniformLocation(program_id, "viewPos")
        glUniform3fv(viewPosLoc, 1, glm.value_ptr(view_origin))

    glBindVertexArray(meshVAO)
    if (key_flags & LIGHTING_FLAG == LIGHTING_FLAG and key_flags & GOURAUD_FLAG == 0):
        glDrawArrays(GL_TRIANGLES, 0, terrain.mesh.triangles.size*3*3)
    else:
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

    if(key_flags & NORMAL_ARROW_FLAG == NORMAL_ARROW_FLAG):
        glBindVertexArray(arrowsVAO)
        glDrawArrays(GL_LINES, 0, normal_arrows.size)

    glutSwapBuffers()


if __name__ == "__main__":
    if(len(sys.argv)!=3):
        print("Usage: ./terreno.py <path to image> <mode>")
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
