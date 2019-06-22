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
VAO = VBO = NBO = 0
program_id = 0
vertex_shader = open("shading.vert").read()
fragment_shader = open("shading.frag").read()

object_transform = glm.mat4(1)
view_origin = glm.vec3(0,0,1)
yaw = pi
pitch = pi/2
view_matrix = glm.lookAt(view_origin, glm.vec3(0,0,0), glm.vec3(0,1,0))
perspective_matrix = glm.perspective(glm.radians(110), 16/9, 0.1, 100)

# Cylindrical coordinates
lightRadius = 1
lightAngle = 0
lightHeight = 0
lightPos = glm.vec3(lightRadius*cos(lightAngle),lightHeight,lightRadius*sin(lightAngle))
lightColor = glm.vec3(1,1,1)
objectColor = glm.vec3(1,0.5,0.31)

def Keyboard(key, x, y):
    global view_origin, view_matrix, lightAngle, lightHeight, lightPos
    
    forward_vector = glm.vec3(sin(yaw)*sin(pitch), cos(pitch), cos(yaw)*sin(pitch))
    right_vector = glm.normalize(glm.cross(forward_vector,glm.vec3(0,1,0)))
    if(key==27 or key == b'q' or key == b'Q'):
        sys.exit(0)
    elif(key==b'd'):
        view_origin+=right_vector*0.1
    elif(key==b'a'):
        view_origin+=right_vector*-0.1
    elif(key==b'w'):
        view_origin+=forward_vector*0.1
    elif(key==b's'):
        view_origin+=forward_vector*-0.1
    elif(key==b' '):
        view_origin+=glm.vec3(0,0.1,0)
    elif(key==b'c'):
        view_origin+=glm.vec3(0,-0.1,0)
    elif(key==b'j'):
        lightAngle+=0.0525
    elif(key==b'l'):
        lightAngle-=0.0525
    elif(key==b'i'):
        lightHeight+=0.1
    elif(key==b'k'):
        lightHeight-=0.1
    
    
    view_matrix = glm.lookAt(view_origin, view_origin + forward_vector, glm.vec3(0,1,0))
    lightPos = glm.vec3(lightRadius*cos(lightAngle),lightHeight,lightRadius*sin(lightAngle))
    print(lightPos)
    glutPostRedisplay()

def SpecialKeys(key, x, y):
    global yaw, pitch, view_matrix

    if(key==GLUT_KEY_LEFT):
        yaw+=0.0525
    elif(key==GLUT_KEY_RIGHT):
        yaw-=0.0525
    elif(key==GLUT_KEY_UP and pitch > 0.0525):
        pitch-=0.0525
    elif(key==GLUT_KEY_DOWN and pitch < pi-0.0525):
        pitch+=0.0525
    
    forward_vector = glm.vec3(sin(yaw)*sin(pitch), cos(pitch), cos(yaw)*sin(pitch))
    view_matrix = glm.lookAt(view_origin, view_origin + forward_vector, glm.vec3(0,1,0))
    glutPostRedisplay()
        

def Init():
    global VAO, VBO, NBO
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    vertices = np.array([
        -0.5, -0.5, -0.5,
         0.5,  0.5, -0.5,
         0.5, -0.5, -0.5,
        -0.5,  0.5, -0.5,
         0.5,  0.5, -0.5,
        -0.5, -0.5, -0.5,

        -0.5, -0.5,  0.5,
         0.5, -0.5,  0.5,
         0.5,  0.5,  0.5,
         0.5,  0.5,  0.5,
        -0.5,  0.5,  0.5,
        -0.5, -0.5,  0.5,

        -0.5,  0.5,  0.5,
        -0.5,  0.5, -0.5,
        -0.5, -0.5, -0.5,
        -0.5, -0.5, -0.5,
        -0.5, -0.5,  0.5,
        -0.5,  0.5,  0.5,

         0.5,  0.5, -0.5,
         0.5,  0.5,  0.5,
         0.5, -0.5, -0.5,
         0.5, -0.5, -0.5,
         0.5,  0.5,  0.5,
         0.5, -0.5,  0.5,

        -0.5, -0.5, -0.5,
         0.5, -0.5, -0.5,
         0.5, -0.5,  0.5,
         0.5, -0.5,  0.5,
        -0.5, -0.5,  0.5,
        -0.5, -0.5, -0.5,

        -0.5,  0.5, -0.5,
         0.5,  0.5,  0.5,
         0.5,  0.5, -0.5,
        -0.5,  0.5,  0.5,
         0.5,  0.5,  0.5,
        -0.5,  0.5, -0.5
    ],dtype=np.float32)
		
    colors = np.array([
        0.483, 0.596, 0.789,
        0.483, 0.596, 0.789,
        0.483, 0.596, 0.789,
        0.483, 0.596, 0.789,
        0.483, 0.596, 0.789,
        0.483, 0.596, 0.789,
		
        0.673, 0.211, 0.457,
        0.673, 0.211, 0.457,
        0.673, 0.211, 0.457,
        0.673, 0.211, 0.457,
        0.673, 0.211, 0.457,
        0.673, 0.211, 0.457,
		
        0.014, 0.184, 0.576,
        0.014, 0.184, 0.576,
        0.014, 0.184, 0.576,
        0.014, 0.184, 0.576,
        0.014, 0.184, 0.576,
        0.014, 0.184, 0.576,
		
        0.055, 0.953, 0.042,
        0.055, 0.953, 0.042,
        0.055, 0.953, 0.042,
        0.055, 0.953, 0.042,
        0.055, 0.953, 0.042,
        0.055, 0.953, 0.042,
		
        0.676, 0.977, 0.133,
        0.676, 0.977, 0.133,
        0.676, 0.977, 0.133,
        0.676, 0.977, 0.133,
        0.676, 0.977, 0.133,
        0.676, 0.977, 0.133,
		
        0.997, 0.513, 0.064,
        0.997, 0.513, 0.064,
        0.997, 0.513, 0.064,
        0.997, 0.513, 0.064,
        0.997, 0.513, 0.064,
        0.997, 0.513, 0.064,
    ], dtype=np.float32)

    normals = np.array([])
    
    # 3 floats per vertex, 3 vertices per triangle
    for i in range(len(vertices)//9):
        # For P, Q, R, defined counter-clockwise, glm.cross(R-Q, P-Q)
        RQ = glm.vec3(vertices[9*i+6]-vertices[9*i+3],vertices[9*i+7]-vertices[9*i+4],vertices[9*i+8]-vertices[9*i+5])
        PQ = glm.vec3(vertices[9*i]-vertices[9*i+3],vertices[9*i+1]-vertices[9*i+4],vertices[9*i+2]-vertices[9*i+5])
        normal = glm.cross(RQ,PQ)
        # Insert once for each vertex
        normals=np.append(normals, [normal.x,normal.y,normal.z]*3)

    normals = normals.astype(np.float32)

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(vertices), vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)
    #glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6*4, 3*4)
    #glEnableVertexAttribArray(1)
    
    NBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, NBO)
    glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(normals), normals, GL_STATIC_DRAW)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(1)
	
    CBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, CBO)
    glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(colors), colors, GL_STATIC_DRAW)
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(2)
    
    global program_id
    program = ShaderProgram(vertex_shader, fragment_shader)
    program_id = program.program_id
    glUseProgram(program_id)
            
    glEnable(GL_DEPTH_TEST)


def Display():
    global perspective_matrix, view_matrix, program_id

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Load shader uniforms
    modelLoc = glGetUniformLocation(program_id, "model")
    glUniformMatrix4fv(modelLoc, 1, GL_FALSE, glm.value_ptr(object_transform))
    viewLoc = glGetUniformLocation(program_id, "view")
    glUniformMatrix4fv(viewLoc, 1, GL_FALSE, glm.value_ptr(view_matrix))
    projectionLoc = glGetUniformLocation(program_id, "projection")
    glUniformMatrix4fv(projectionLoc, 1, GL_FALSE, glm.value_ptr(perspective_matrix))

    objColorLoc = glGetUniformLocation(program_id, "objectColor")
    glUniform3fv(objColorLoc, 1, glm.value_ptr(objectColor))
    lightColorLoc = glGetUniformLocation(program_id, "lightColor")
    glUniform3fv(lightColorLoc, 1, glm.value_ptr(lightColor))
    lightPosLoc = glGetUniformLocation(program_id, "lightPos")
    glUniform3fv(lightPosLoc, 1, glm.value_ptr(lightPos))
    viewPosLoc = glGetUniformLocation(program_id, "viewPos")
    glUniform3fv(viewPosLoc, 1, glm.value_ptr(view_origin))

    glBindVertexArray(VAO)
    glDrawArrays(GL_TRIANGLES, 0, 12*3);
    
    glutSwapBuffers()


if __name__ == "__main__":
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(1600, 900)
    glutInitContextVersion(3, 3)
    glutInitContextProfile(GLUT_CORE_PROFILE)
    glutCreateWindow(bytes(sys.argv[0], 'utf-8'))

    Init()
    glutKeyboardFunc(Keyboard)
    glutSpecialFunc(SpecialKeys)
    glutDisplayFunc(Display)

    glutMainLoop()
