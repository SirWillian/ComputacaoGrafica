#!/usr/bin/env python
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

object_transform = 0
view_origin = glm.vec3(0,0,-1)
yaw = pi/2
pitch = pi/2
view_matrix = glm.lookAt(view_origin, view_origin + glm.vec3(0,0,1), glm.vec3(0,1,0))
perspective_matrix = glm.perspective(glm.radians(110), 1, 0.1, 100)

def process_arguments(args):
    arg_pos = 1
    transforms = []
    for i in range(2):
        argument = int(args[arg_pos])
        trans = glm.mat4(1)
        if argument < 1 or argument > 5:
            print("Invalid arguments")
            sys.exit(0)
        elif argument < 4:
            axis = np.zeros(3)
            axis[argument-1] = 1
            
            trans = glm.rotate(trans, glm.radians(float(args[arg_pos+1])), glm.vec3(axis))
            
            arg_pos += 2
        else:
            transform_params = np.array(args[arg_pos+1:arg_pos+4],dtype=float)
            
            if argument == 4:
                trans = glm.translate(trans,transform_params)
            else:
                trans = glm.scale(trans,transform_params)
            
            arg_pos += 4
            
        print("Transformação "+str(i+1))
        print(trans)
        transforms.append(trans)
        
    return transforms[1]*transforms[0]
            
            

def Keyboard(key, x, y):
    global view_origin, view_matrix
    
    forward_vector = glm.vec3(cos(yaw)*sin(pitch), cos(pitch), sin(yaw)*sin(pitch))
    right_vector = glm.normalize(glm.cross(glm.vec3(0,1,0),forward_vector))
    if(key==27 or key == b'q' or key == b'Q'):
        sys.exit(0)
    elif(key==b'd'):
        view_origin+=right_vector*-0.1
    elif(key==b'a'):
        view_origin+=right_vector*0.1
    elif(key==b'w'):
        view_origin+=forward_vector*0.1
    elif(key==b's'):
        view_origin+=forward_vector*-0.1
    elif(key==b' '):
        view_origin+=glm.vec3(0,0.1,0)
    elif(key==b'c'):
        view_origin+=glm.vec3(0,-0.1,0)
    
    view_matrix = glm.lookAt(view_origin, view_origin + forward_vector, glm.vec3(0,1,0))
    glutPostRedisplay()

def SpecialKeys(key, x, y):
    global yaw, pitch, view_matrix

    if(key==GLUT_KEY_LEFT):
        yaw-=0.0525
    elif(key==GLUT_KEY_RIGHT):
        yaw+=0.0525
    elif(key==GLUT_KEY_UP and pitch > 0.0525):
        pitch-=0.0525
    elif(key==GLUT_KEY_DOWN and pitch < pi-0.0525):
        pitch+=0.0525
    
    forward_vector = glm.vec3(cos(yaw)*sin(pitch), cos(pitch), sin(yaw)*sin(pitch))
    view_matrix = glm.lookAt(view_origin, view_origin + forward_vector, glm.vec3(0,1,0))
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

    colors = np.array([
        0.583, 0.771, 0.014, 1.0,
        0.609, 0.115, 0.436, 1.0,
        0.327, 0.483, 0.844, 1.0,
        0.822, 0.569, 0.201, 1.0,
        0.435, 0.602, 0.223, 1.0,
        0.310, 0.747, 0.185, 1.0,
        0.597, 0.770, 0.761, 1.0,
        0.559, 0.436, 0.730, 1.0,
        0.359, 0.583, 0.152, 1.0,
        0.483, 0.596, 0.789, 1.0,
        0.559, 0.861, 0.639, 1.0,
        0.195, 0.548, 0.859, 1.0,
        0.014, 0.184, 0.576, 1.0,
        0.771, 0.328, 0.970, 1.0,
        0.406, 0.615, 0.116, 1.0,
        0.676, 0.977, 0.133, 1.0,
        0.971, 0.572, 0.833, 1.0,
        0.140, 0.616, 0.489, 1.0,
        0.997, 0.513, 0.064, 1.0,
        0.945, 0.719, 0.592, 1.0,
        0.543, 0.021, 0.978, 1.0,
        0.279, 0.317, 0.505, 1.0,
        0.167, 0.620, 0.077, 1.0,
        0.347, 0.857, 0.137, 1.0,
        0.055, 0.953, 0.042, 1.0,
        0.714, 0.505, 0.345, 1.0,
        0.783, 0.290, 0.734, 1.0,
        0.722, 0.645, 0.174, 1.0,
        0.302, 0.455, 0.848, 1.0,
        0.225, 0.587, 0.040, 1.0,
        0.517, 0.713, 0.338, 1.0,
        0.053, 0.959, 0.120, 1.0,
        0.393, 0.621, 0.362, 1.0,
        0.673, 0.211, 0.457, 1.0,
        0.820, 0.883, 0.371, 1.0,
        0.982, 0.099, 0.879, 1.0
    ], dtype=np.float32)

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(vertices), vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)
    
    CBO = glGenBuffers(1);
    glBindBuffer(GL_ARRAY_BUFFER, CBO)
    glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(colors), colors, GL_STATIC_DRAW)
    glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(1)
    
    global program_id
    program = ShaderProgram(vertex_shader, fragment_shader)
    program_id = program.program_id
    glUseProgram(program_id)

    global object_transform
    object_transform = process_arguments(sys.argv)
    print("Transformações combinadas")
    print(object_transform)
            
    glEnable(GL_DEPTH_TEST)


def Display():
    global perspective_matrix, object_transform, view_matrix, program_id

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    transform = perspective_matrix * view_matrix * object_transform

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
    glutSpecialFunc(SpecialKeys)
    glutDisplayFunc(Display)

    glutMainLoop()
