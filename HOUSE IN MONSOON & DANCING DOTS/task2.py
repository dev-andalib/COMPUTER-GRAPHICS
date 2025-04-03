##################################################################
#TASK2
####################################################################
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random


#GLOBAL VARS
blink_track = False
ballx = bally = 0
step_size = 0.0001
temp_step_size = step_size
ball_size = 2
W_Width = 1200
W_Height = 600
point_store = [] # to store points

def reflect(n):
    global point_store
    point = point_store[n]

    if point[3] == 0:
        if point[0] >= 1 and point[1] >= 1:
            point[3] = 2
        elif point[0] >= 1:
            point[3] = 3
        elif point[1] >= 1:
            point[3] = 1

    elif point[3] == 1:
        if point[0] >= 1 and point[1] <= -1:
            point[3] = 3
        elif point[0] >= 1:
            point[3] = 2
        elif point[1] <= -1:
            point[3] = 0

    elif point[3] == 2:
        if point[0] <= -1 and point[1] <= -1:
            point[3] = 0
        elif point[0] <= -1:
            point[3] = 1
        elif point[1] <= -1:
            point[3] = 3



    elif point[3] == 3:
        if point[0] <= -1 and point[1] >= 1:
            point[3] = 1
        elif point[0] <= -1:
            point[3] = 0
        elif point[1] >= 1:
            point[3] = 2

    point_store[n] = point



def letsDraw():
    global  point_store, blink_track
    glPointSize(20)  # pixel size. by default 1 thake
    glBegin(GL_POINTS)
    for point in point_store:

        if blink_track == False:
            glColor3f(point[2][0], point[2][1], point[2][2])

        elif blink_track == True:
            glColor3f(0,0,0)

        glVertex2f(point[0], point[1])
        reflect(point_store.index(point))
    glEnd()



def convert_coordinate(x,y):
    global W_Width, W_Height
    x_cor = (2*x - W_Width)/W_Width
    y_cor = (W_Height - 2*y)/W_Height
    return (x_cor, y_cor)


def mouseCommand(btn, state, x, y):
    global ballx, bally, point_store, blink_track
    numbers = [0, 1, 2, 3]
    direction = random.choice(numbers)

    if btn == GLUT_RIGHT_BUTTON:
        if state == GLUT_UP:
            ballx, bally = convert_coordinate(x, y)
            r = random.uniform(0,1)
            g = random.uniform(0,1)
            b = random.uniform(0, 1)
            point_store.append([ballx, bally, (r, g, b), direction])
            glutPostRedisplay()

    elif btn == GLUT_LEFT_BUTTON and blink_track == False:
        if state == GLUT_UP:
            blink_track = True

    elif btn == GLUT_LEFT_BUTTON and blink_track:
        if state == GLUT_UP:
            blink_track = False


def keypress(key,x,y):
    global step_size
    if key == GLUT_KEY_UP and step_size <= 0.01:
        step_size *= 5
    elif key == GLUT_KEY_DOWN and step_size >= 0.0001:
        step_size /= 5


def spacehit(key, x, y):
    global step_size, temp_step_size
    if key == b' ' and step_size != 0:
        temp_step_size = step_size
        step_size = 0
    elif key == b' ' and step_size == 0:
        step_size = temp_step_size


def movement():
    global  point_store
    for point in point_store:
        if point[3] == 0:
            point[0] += step_size
            point[1] += step_size


        elif point[3] == 1:
            point[0] += step_size
            point[1] -= step_size

        elif point[3] == 2:
            point[0] -= step_size
            point[1] -= step_size

        elif point[3] == 3:
            point[0] -= step_size
            point[1] += step_size
    glutPostRedisplay()



def start():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1, 1, -1, 1)

def showStuff():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    letsDraw()
    glutSwapBuffers()





glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"TASK 2")


start()


glutDisplayFunc(showStuff)
glutIdleFunc(movement)
glutSpecialFunc(keypress)
glutMouseFunc(mouseCommand)
glutKeyboardFunc(spacehit)

glutMainLoop()