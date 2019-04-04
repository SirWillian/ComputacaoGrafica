import numpy as np
from OpenGL.arrays import ArrayDatatype
from OpenGL.GL import *
from OpenGL.GLUT import *
import sys
sys.path.append('../../lib')

from Vec3 import Vec3
from Point import Point
from ShaderProgram import ShaderProgram

WINDOW_SIZE = 512

vertex_shader = open("simple.vert").read()
fragment_shader = open("simple.frag").read()
vao_id = 0
vbo_id = 0

point_data = [Point(0,0,0)]*3
click_count = 0

def mouse_callback(button, state, xc, yc):
    if(button==GLUT_LEFT_BUTTON and state==GLUT_DOWN):
        global click_count, point_data
        if(click_count < 3):
            print("Click on "+str(xc)+" "+str(yc))
            x = 2*xc/WINDOW_SIZE - 1
            y = (-2*yc/WINDOW_SIZE + 1)
            print("OpenGL Coordinates: "+str(x)+" "+str(y))
            
            point_data[click_count]=Point(x,y)
            click_count = (click_count+1)
            
            glBindBuffer(GL_ARRAY_BUFFER, vbo_id)
            
            if(click_count < 3):
                vertex_data = np.array([point.coordinates for point in point_data], dtype=np.float32).ravel()
                glBufferSubData(GL_ARRAY_BUFFER, 0, 12*click_count, vertex_data)
            else:
                u = point_data[0]-point_data[1]
                v = point_data[2]-point_data[1]
                vertex_data = np.concatenate([point_data[0].coordinates,point_data[1].coordinates,
                                              point_data[1].coordinates, point_data[2].coordinates]).astype(np.float32)
                
                print("\nu: "+str(u.coordinates)+" v: "+str(v.coordinates))
                print("Angulo entre u v: "+str(Vec3.angle_between(u,v)))
                print("u.v = "+str(Vec3.dot(u,v))+" u x v = "+str(Vec3.cross(u,v).coordinates)+"\n")
                print("Distância de P a v = "+str(Vec3.cross(u,v).norm()/v.norm()))

                glBufferSubData(GL_ARRAY_BUFFER, 0, 12*4, vertex_data)
            print(vertex_data)                
        else:
            point_data = [Point(0,0,0)]*3
            click_count = 0
            glBindBuffer(GL_ARRAY_BUFFER, vbo_id)
            glBufferData(GL_ARRAY_BUFFER, 12*4, None, GL_STATIC_DRAW)
        
def display():
    glClear(GL_COLOR_BUFFER_BIT)
        
    glBindVertexArray(vao_id)
    if(click_count<3):
        glDrawArrays(GL_POINTS, 0, click_count)
    else:
        glDrawArrays(GL_LINES, 0, 4)
#    glDrawArrays(GL_POINTS, 0, 4)
    glutSwapBuffers()
#    glFlush()


def data_init():
    print("Vertex Shader:\n",vertex_shader)
    print("Fragment Shader:\n",fragment_shader)
    program = ShaderProgram(fragment=fragment_shader, vertex=vertex_shader)

    vao_id = glGenVertexArrays(1)
    glBindVertexArray(vao_id)

    vbo_id = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo_id)
    glBufferData(GL_ARRAY_BUFFER, 12*4, None, GL_STATIC_DRAW)

    pos_attrib = program.attribute_location('vPosition')    
    glEnableVertexAttribArray(pos_attrib)
    glVertexAttribPointer(pos_attrib, 3, GL_FLOAT, GL_FALSE, 0, None)

    glUseProgram(program.program_id)

    return vao_id, vbo_id, program

if __name__ == "__main__":
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(WINDOW_SIZE,WINDOW_SIZE)
    glutInitContextVersion(3,3)
    glutInitContextProfile(GLUT_CORE_PROFILE)
    glutCreateWindow(b"Lista 1 - Exercicio 11")
    vao_id, vbo_id, program = data_init()

    glutMouseFunc(mouse_callback)

    glutDisplayFunc(display)

    glutMainLoop()
