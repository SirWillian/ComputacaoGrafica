from glfw import *
import numpy as np
from OpenGL.arrays import ArrayDatatype
from OpenGL.GL import *
import sys
sys.path.append('../../lib')

from Vec3 import Vec3
from Point import Point
from ShaderProgram import ShaderProgram

SCREEN_SIZE = 800

vertex_shader = open("simple.vert").read()
fragment_shader = open("simple.frag").read()
vao_id = 0
vbo_id = 0

point_data = [Point(0,0,0)]*3
click_count = 0

def mouse_callback(window, button, action, mods):
    if(button==MOUSE_BUTTON_1 and action==PRESS):
        xc, yc = get_cursor_pos(window)

        global click_count, point_data
        if(click_count < 3):
            print("Click on "+str(xc)+" "+str(yc))
            x = 2*xc/SCREEN_SIZE - 1
            y = (-2*yc/SCREEN_SIZE + 1)
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

                glBufferSubData(GL_ARRAY_BUFFER, 0, 12*4, vertex_data)
            print(vertex_data)                
        else:
            point_data = [Point(0,0,0)]*3
            click_count = 0
            glBindBuffer(GL_ARRAY_BUFFER, vbo_id)
            glBufferData(GL_ARRAY_BUFFER, 12*4, None, GL_STATIC_DRAW)
        
    

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
    if not init():
        print ('GLFW initialization failed')
        sys.exit(-1)
    window_hint(CONTEXT_VERSION_MAJOR, 3)
    window_hint(CONTEXT_VERSION_MINOR, 2)
    window_hint(OPENGL_PROFILE, OPENGL_CORE_PROFILE)
    window_hint(OPENGL_FORWARD_COMPAT, GL_TRUE)

    window = create_window(SCREEN_SIZE, SCREEN_SIZE, "Lista 1 - Exercicio 7", None, None)
    if not window:
        print ("OpenWindow failed")
        terminate()
        sys.exit(-1)

    make_context_current(window)
    vao_id, vbo_id, program = data_init()

    set_mouse_button_callback(window, mouse_callback)

    running = True

    while running:
        glClear(GL_COLOR_BUFFER_BIT)
        
        glBindVertexArray(vao_id)
        if(click_count<3):
            glDrawArrays(GL_POINTS, 0, click_count)
        else:
            glDrawArrays(GL_LINES, 0, 4)

        swap_buffers(window)
        poll_events()

        # If the user has closed the window in anger
        # then terminate this program
        running = running and window_should_close(window)==0
