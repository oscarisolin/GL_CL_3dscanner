import numpy as np
from OpenGL.GL import (
    GL_FRAGMENT_SHADER, GL_VERTEX_SHADER, GL_VERTEX_ARRAY, GL_COLOR_ARRAY, GL_FALSE, GL_INT,GL_COLOR_ARRAY,
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT,  GL_FLOAT, GL_MODELVIEW_MATRIX, GL_ARRAY_BUFFER,
    glClear, glViewport, 
    shaders, glEnableClientState, glGetUniformLocation, glUniform4f,glUniformMatrix4fv, 
    glVertexPointer, glColorPointer,
    glDrawArrays, glPointSize, glGetDoublev, 
    GL_TRIANGLES, GL_POINTS, GL_TRIANGLE_STRIP,
    glRotatef, glTranslatef, glScalef,
    glPushMatrix, glPopMatrix, glVertexAttribPointer, glEnableVertexAttribArray, glDisableVertexAttribArray
    )
from OpenGL.GLUT import (
    GLUT_RGBA,GLUT_DEPTH, GLUT_DOUBLE, GLUT_RGB,
    glutInit, glutInitDisplayMode, glutDisplayFunc, glutIdleFunc, glutMouseFunc,
    glutInitWindowSize, glutInitWindowPosition, glutCreateWindow, 
    glutMainLoop, glutSwapBuffers
)
# from OpenGL.GLU import *
from OpenGL.arrays import vbo

import cv2

# Load an color image in grayscale
img = cv2.imread('photo.jpg')
print(img.shape)

xkord, ykord = np.indices((img.shape[0],img.shape[1]))
xkord = np.expand_dims(xkord,axis=2)
ykord = np.expand_dims(ykord,axis=2)
zkord = np.ones_like(xkord)
xykoords = np.append(xkord,ykord,axis=2)
koords = np.append(xykoords,zkord,axis=2)
img = np.append(koords,img,axis=2)
imgnp = np.array(img, dtype=np.float32)

# for i in range(1000):
#    imgnp[i,0,3] = 0.5
#    imgnp[i,0,4] = 0.0
#    imgnp[i,0,5] = 0.0

def draw_points():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnableClientState(GL_VERTEX_ARRAY)
    # glVertexPointer(3, GL_FLOAT, 24, points)
    # glColorPointer(3, GL_INT, 24, points+12)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, points)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, points+12)
    glEnableVertexAttribArray(1)
    
    glDrawArrays(GL_POINTS,0,imgnp.shape[0]*imgnp.shape[1])

    glDisableVertexAttribArray(0)
    glDisableVertexAttribArray(1)
    glutSwapBuffers()

def moveMouse(x,y,z,w):
    pass


glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
glutInitWindowSize(500, 500)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("OpenGL Window")
glPointSize(1)

vertshader = shaders.compileShader(
    """
    #version 330 core    
    layout (location = 0) in vec3 aPos;
    layout (location = 1) in vec3 aColor;

    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;

    out vec3 ourColor;

    void main()
    {
       gl_Position = model * vec4(aPos, 1.0);
       ourColor = vec3(aColor/255);       
    }    
    """,
    shaderType=GL_VERTEX_SHADER
    )

fragshader = shaders.compileShader(
    """
    #version 330 core

    in vec3 ourColor;

    void main() {
        gl_FragColor = vec4(ourColor, 1.0);
    }
    """,
    shaderType=GL_FRAGMENT_SHADER
)

shaderProg = shaders.compileProgram(vertshader, fragshader)
shaders.glUseProgram(shaderProg)

points = vbo.VBO(data=imgnp, usage="GL_DYNAMIC_DRAW",target='GL_ARRAY_BUFFER', size=None)
points.bind()

modelmat = glGetUniformLocation(shaderProg, 'model')
viewmat = glGetUniformLocation(shaderProg, 'view')
projectionmat = glGetUniformLocation(shaderProg, 'projection')

glPushMatrix()
glRotatef(-90, 0, 0, 1) 

scal = 0.01
glTranslatef(-0.5 , -0.5, 0)
glScalef(1/imgnp.shape[0], 1/imgnp.shape[1], 1)
model2 = glGetDoublev(GL_MODELVIEW_MATRIX)
glPopMatrix()
# print(model2)

glUniformMatrix4fv(modelmat,1, GL_FALSE, model2)

glutDisplayFunc(draw_points)

# glutInitWindowPosition(600, 100)
# wind2 = glutCreateWindow("OpenGL Window2")
# glutMouseFunc(moveMouse)
glutMainLoop()
