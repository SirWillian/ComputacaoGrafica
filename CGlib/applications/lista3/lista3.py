import numpy as np
from OpenGL.arrays import ArrayDatatype
from OpenGL.GL import *
from OpenGL.GLUT import *
import glm
import sys
from ShaderProgram import ShaderProgram


# Globals
VAO = VBO = CBO = 0
vertex_shader = open("simple3.vert").read()
fragment_shader = open("simple3.frag").read()

def Keyboard(key, x, y):
    if(key==27 or key == b'q' or key == b'Q'):
        sys.exit(0)


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
    
    program = ShaderProgram(vertex_shader, fragment_shader)
    glUseProgram(program.program_id)

    trans = glm.mat4(1)
    trans = glm.rotate(trans, glm.radians(45.0), glm.vec3(0.0, 0.0, 1.0))
    trans = glm.rotate(trans, glm.radians(30.0), glm.vec3(0.0, 1.0, 0.0))
    trans = glm.rotate(trans, glm.radians(15.0), glm.vec3(1.0, 0.0, 0.0))
    print(trans)
    
    transformLoc = glGetUniformLocation(program.program_id, "transform")
    glUniformMatrix4fv(transformLoc, 1, GL_FALSE, glm.value_ptr(trans))
            
    glEnable(GL_DEPTH_TEST)


def Display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glBindVertexArray(VAO)
    glDrawArrays(GL_TRIANGLES, 0, 12*3);
    #glDrawArrays(GL_POINTS, 0, 36)

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
