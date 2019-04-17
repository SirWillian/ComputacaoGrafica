from glfw import *
import numpy as np
from OpenGL.arrays import ArrayDatatype
from OpenGL.GL import *
import sys
sys.path.append('../../lib')

from Vec3 import Vec3
from Point import Point
from ShaderProgram import ShaderProgram


vertex_shader = open("simple.vert").read()
fragment_shader = open("simple.frag").read()

vertex_data = np.array([0.75, 0.75, 0.0, 1.0,
                        0.75, -0.75, 0.0, 1.0,
                        -0.75, -0.75, 0.0, 1.0], dtype=np.float32)

vertex_data2 = np.array([Point(0.75, 0.75, 0.0),
                         Point(0.75, -0.75, 0.0),
                         Point(-0.5, -0.75, 0.0)])

color_data = np.array([1, 0, 0, 1,
                        0, 1, 0, 1,
                        0, 0, 1, 1], dtype=np.float32)

def key_callback(key, action):
    """ Sample keyboard callback function """
    print('Key: %s Action: %s pressed' % (key, action))

def data_init():
    # Lets compile our shaders since the use of shaders is now
    # mandatory. We need at least a vertex and fragment shader
    # begore we can draw anything
    print(vertex_shader)
    print(fragment_shader)
    program = ShaderProgram(fragment=fragment_shader, vertex=vertex_shader)

    # Lets create a VAO and bind it
    # Think of VAO's as object that encapsulate buffer state
    # Using a VAO enables you to cut down on calls in your draw
    # loop which generally makes things run faster
    vao_id = glGenVertexArrays(1)
    glBindVertexArray(vao_id)

    # Lets create our Vertex Buffer objects - these are the buffers
    # that will contain our per vertex data
    vbo_id = glGenBuffers(2)

    # Bind a buffer before we can use it
    glBindBuffer(GL_ARRAY_BUFFER, vbo_id[0])

    # Now go ahead and fill this bound buffer with some data
    #vertex_data3=np.array([point.coordinates for point in vertex_data2],dtype=np.float32).ravel()
    glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(vertex_data), vertex_data, GL_STATIC_DRAW)

    pos_attrib = program.attribute_location('vPosition')
    # Turn on this vertex attribute in the shader
    glEnableVertexAttribArray(pos_attrib)
    # Now specify how the shader program will be receiving this data
    # In this case the data from this buffer will be available in the shader as the vPosition vertex attribute
    glVertexAttribPointer(pos_attrib, 4, GL_FLOAT, GL_FALSE, 0, None)

    # Now do the same for the other vertex buffer
    color_attrib = program.attribute_location('vInColor')
    glEnableVertexAttribArray(color_attrib)
    glBindBuffer(GL_ARRAY_BUFFER, vbo_id[1])
    glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(color_data), color_data, GL_STATIC_DRAW)
    glVertexAttribPointer(color_attrib, 4, GL_FLOAT, GL_FALSE, 0, None)

    # Lets unbind our vbo and vao state
    # We will bind these again in the draw loop
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    return vao_id, vbo_id, program

if __name__ == "__main__":
    if not init():
        print ('GLFW initialization failed')
        sys.exit(-1)

    # These Window hints are used to specify
    # which opengl version to use and other details
    # for the opengl context that will be created
    window_hint(CONTEXT_VERSION_MAJOR, 3)
    window_hint(CONTEXT_VERSION_MINOR, 2)
    window_hint(OPENGL_PROFILE, OPENGL_CORE_PROFILE)
    window_hint(OPENGL_FORWARD_COMPAT, GL_TRUE)

    window = create_window(1400, 800, "Modern opengl example", None, None)
    if not window:
        print ("OpenWindow failed")
        terminate()
        sys.exit(-1)

    make_context_current(window)
    
    # Every time a key on the keyboard is clicked
    # call our callback function
    #set_key_callback(key_callback)

    # If everything went well the following calls
    # will display the version of opengl being used
    print ('Vendor: %s' % (glGetString(GL_VENDOR)))
    print ('Opengl version: %s' % (glGetString(GL_VERSION)))
    print ('GLSL Version: %s' % (glGetString(GL_SHADING_LANGUAGE_VERSION)))
    print ('Renderer: %s' % (glGetString(GL_RENDERER)))

    glClearColor(0.0, 0.0, 0.0, 0)

    vao_id, vbo_id, program = data_init()

    running = True

    while running:
        glClear(GL_COLOR_BUFFER_BIT)
        
        # Specify shader to be used
        glUseProgram(program.program_id)
        
        # Bind VAO - this will automatically
        # bind all the vbo's saving us a bunch
        # of calls
        glBindVertexArray(vao_id)

        # Modern GL makes the draw call really simple
        # All the complexity has been pushed elsewhere
        glDrawArrays(GL_TRIANGLES, 0, 3)

        # Lets unbind the shader and vertex array state
        glUseProgram(0)
        glBindVertexArray(0)

        # Now lets show our master piece on the screen
        swap_buffers(window)
        poll_events()

        # If the user has closed the window in anger
        # then terminate this program
        running = running and window_should_close(window)==0
