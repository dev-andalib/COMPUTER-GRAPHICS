from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random



background = {
    "sky":[],
    "land":[],
    "house":[],
    "rain":[[(-1,1),(1, 1),(-1,1/3),(1, 1/3)], (1,1,1)]
}


W_Width = 1400
W_Height = 1400

def convert_coordinate(x,y):
    global W_Width, W_Height
    x_cor = (2*x - W_Width)/W_Width
    y_cor = (W_Height - 2*y)/W_Height
    return (x_cor, y_cor)



def letsDraw():
    global  point_store, blink_track
    glPointSize(5)  # pixel size. by default 1 thake
    glBegin(GL_POINTS)

    glEnd()



def showStuff():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    letsDraw()
    glutSwapBuffers()


def start():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1, 1, -1, 1)


def keypress(key,x,y):
    pass




glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"TASK 1")


start()


glutDisplayFunc(showStuff)
# glutIdleFunc()
glutSpecialFunc(keypress)

# glutKeyboardFunc()

glutMainLoop()