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

vertex_data = np.array([0.75, 0.75, 0.0, 1.0,
                        0.75, -0.75, 0.0, 1.0,
                        -0.75, -0.75, 0.0, 1.0], dtype=np.float32)

color_data = np.array([1, 0, 0, 1,
                        0, 1, 0, 1,
                        0, 0, 1, 1], dtype=np.float32)

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

vec1=Vec3(-1,1)
vec2=Vec3(1,1)
point=Point(2,3)

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
    
    print(vertex_data)
    # ----------
    
    glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(vertices), vertices, GL_STATIC_DRAW)

    pos_attrib = program.attribute_location('vPosition')    
    glEnableVertexAttribArray(pos_attrib)
    glVertexAttribPointer(pos_attrib, 4, GL_FLOAT, GL_FALSE, 0, None)

    color_attrib = program.attribute_location('vInColor')
    glEnableVertexAttribArray(color_attrib)
    glBindBuffer(GL_ARRAY_BUFFER, vbo_id[1])
    glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(colors), colors, GL_STATIC_DRAW)
    glVertexAttribPointer(color_attrib, 4, GL_FLOAT, GL_FALSE, 0, None)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    glUseProgram(program.program_id)
    #glEnable(GL_DEPTH_TEST)

    return vao_id, vbo_id, program

def display():
    glClear(GL_COLOR_BUFFER_BIT)
        
    glBindVertexArray(vao_id)
    glDrawArrays(GL_TRIANGLES, 0, 36)

    glutSwapBuffers()

if __name__ == "__main__":
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_SIZE,WINDOW_SIZE)
    glutInitContextVersion(3,3)
    glutInitContextProfile(GLUT_CORE_PROFILE)
    glutCreateWindow(b"Lista 1 - Exercicio 1")

    vao_id, vbo_id, program = data_init()

    glutDisplayFunc(display)

    glutMainLoop()
