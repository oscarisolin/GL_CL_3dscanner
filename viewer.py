import numpy as np
from OpenGL.GL import (
    GL_FRAGMENT_SHADER, GL_VERTEX_SHADER, GL_VERTEX_ARRAY,
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT,  GL_FLOAT,
    glClear, glViewport,
    shaders, glEnableClientState, glVertexPointer,
    glDrawArrays, glPointSize,
    GL_TRIANGLES, GL_POINTS, GL_TRIANGLE_STRIP
    )
from OpenGL.GLUT import (
    GLUT_RGBA,GLUT_DEPTH, GLUT_DOUBLE,
    glutInit, glutInitDisplayMode, glutDisplayFunc, glutIdleFunc, glutMouseFunc,
    glutInitWindowSize, glutInitWindowPosition, glutCreateWindow, 
    glutMainLoop, glutSwapBuffers
)
# from OpenGL.GLU import *
from OpenGL.arrays import vbo


def draw_points():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glDrawArrays(GL_POINTS,0,5)

    glutSwapBuffers()

def moveMouse(x,y,z,w):
    pass


glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
glutInitWindowSize(500, 500)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("OpenGL Window")
glPointSize(4)

vertshader = shaders.compileShader(
    """
    #version 330 core    
    layout (location = 0) in vec3 aPos;
    void main()
    {
       gl_Position = vec4(aPos, 1.0);
    }    
    """,
    shaderType=GL_VERTEX_SHADER
    )

fragshader = shaders.compileShader(
    """
    #version 330 core
    void main() {
        gl_FragColor = vec4(0.5, 0.0, 0.0, 1.0);
    }
    """,
    shaderType=GL_FRAGMENT_SHADER
)

shaderProg = shaders.compileProgram(vertshader, fragshader)
shaders.glUseProgram(shaderProg)

point_array = np.array(
    [
        [0.5, 0.5, 0.5], 
        [0.7, 0.5, 0.5], 
        [0.7, 0.7, 0.5], 
        [0.0, 0.0, 0.0], 
        [-0.5, 0.0, 0.0]
    ], 
    dtype=np.float32
    )

points = vbo.VBO(data=point_array, usage="GL_DYNAMIC_DRAW",target='GL_ARRAY_BUFFER', size=None)
points.bind()

glEnableClientState(GL_VERTEX_ARRAY)
glVertexPointer(3, GL_FLOAT, 12, points)


glutDisplayFunc(draw_points)


glutInitWindowPosition(600, 100)
# wind2 = glutCreateWindow("OpenGL Window2")
# glutMouseFunc(moveMouse)
glutMainLoop()
