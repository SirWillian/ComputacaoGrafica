import numpy as np
from OpenGL.arrays import ArrayDatatype
from OpenGL.GL import *
from OpenGL.GLUT import *
import sys
sys.path.append('../../lib')

from Vec3 import Vec3
from Point import Point
from ShaderProgram import ShaderProgram

WINDOW_SIZE=512

vertex_shader = open("colored.vert").read()
fragment_shader = open("colored.frag").read()

vec1=Vec3(-1,1)
vec2=Vec3(1,1)

u=Vec3(3,1)
v=Vec3(0,2)

def data_init():
    print("Vertex Shader:\n",vertex_shader)
    print("Fragment Shader:\n",fragment_shader)
    program = ShaderProgram(fragment=fragment_shader, vertex=vertex_shader)

    vao_id = glGenVertexArrays(1)
    glBindVertexArray(vao_id)

    vbo_id = glGenBuffers(2)
    glBindBuffer(GL_ARRAY_BUFFER, vbo_id[0])

    # Now go ahead and fill this bound buffer with some data
    vertex_data1=np.concatenate([[0,0,0],vec1.coordinates/4,
                                vec1.coordinates/4,(vec1+vec2).coordinates/4,
                                [0,0,0],(vec1+vec2).coordinates/4]).astype(np.float32)
    color_data1 = np.array([1, 1, 1, 1, 1, 1,
                            1, 1, 1, 1, 1, 1,
                            1, 1, 0, 1, 1, 0], dtype=np.float32)

    vertex_data2a=np.concatenate([[0,0,0],u.coordinates/4,
                                 u.coordinates/4,(u+v).coordinates/4,
                                 [0,0,0],(u+v).coordinates/4]).astype(np.float32)
    color_data2a = np.array([0,1,0.5,0,1,0.5,
                            0,1,1,0,1,1,
                            1,1,0,1,1,0], dtype=np.float32)
    
    vertex_data2b=np.concatenate([u.coordinates/4,(u-v).coordinates/4,
                                  [0,0,0],(u-v).coordinates/4]).astype(np.float32)
    color_data2b = np.array([0,1,0,0,1,0,
                             1,1,0,1,1,0], dtype=np.float32)

    vertex_data = np.concatenate([vertex_data1, vertex_data2a, vertex_data2b])
    color_data = np.concatenate([color_data1, color_data2a, color_data2b])
    print(vertex_data)
    # ----------
    
    glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(vertex_data), vertex_data, GL_STATIC_DRAW)

    pos_attrib = program.attribute_location('vPosition')    
    glEnableVertexAttribArray(pos_attrib)
    glVertexAttribPointer(pos_attrib, 3, GL_FLOAT, GL_FALSE, 0, None)

    color_attrib = program.attribute_location('vInColor')
    glEnableVertexAttribArray(color_attrib)
    glBindBuffer(GL_ARRAY_BUFFER, vbo_id[1])
    glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(color_data), color_data, GL_STATIC_DRAW)
    glVertexAttribPointer(color_attrib, 3, GL_FLOAT, GL_FALSE, 0, None)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    glUseProgram(program.program_id)

    return vao_id, vbo_id, program

def display():
    glClear(GL_COLOR_BUFFER_BIT)
        
    glBindVertexArray(vao_id)
    glDrawArrays(GL_LINES, 0, 16)

    glutSwapBuffers()

if __name__ == "__main__":
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(WINDOW_SIZE,WINDOW_SIZE)
    glutInitContextVersion(3,3)
    glutInitContextProfile(GLUT_CORE_PROFILE)
    glutCreateWindow("Lista 1 - Exercícios 1 e 2")

    vao_id, vbo_id, program = data_init()

    glutDisplayFunc(display)

    glutMainLoop()
