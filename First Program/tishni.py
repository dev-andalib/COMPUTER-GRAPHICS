from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

W_Width, W_Height = 1000,500
speed=0.05
points=[]
pause=False
blink=False


class Point:
    def __init__(self,x,y,x_speed, y_speed,clr):
        self.x=x
        self.y=y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.color=clr


def draw_points():
    glPointSize(6) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    #glVertex2f(x,y) #jekhane show korbe pixel
    for i in points:
        glColor3f(1, 0, 1)
        glVertex2f(i.x, i.y)
        print(i.x, i.y)
    glEnd()



def mouse_connection(button, state, x, y):	#/#/x, y is the x-y of the screen (2D)
    global blink
    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:  # // 2 times?? in ONE click? -- solution is checking DOWN or UP
           c_x = x
           c_y = y
           color = [random.random(), random.random(), random.random()]
           x_speed = random.uniform(-speed, speed)
           y_speed = random.uniform(-speed, speed)
           points.append(Point(c_x, c_y, color, x_speed, y_speed))


    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            blink = not blink

    glutPostRedisplay()

def keyboard_connection(key,x,y): #pause_unpause
    global speed,pause,points

    if key==b' ':
        if not pause:
            pause= True
            for i in points:
                i.x_speed=0
                i.y_speed=0
        else:
            pause=False
            for i in points:
                i.x_speed = random.uniform(-speed, speed)
                i.y_speed = random.uniform(-speed, speed)#to get the previous speed ager velocity store kora lagbe


def arrow_Key_connection(key, x, y):
    global speed

    if key==GLUT_KEY_UP:
        speed *= 2
        print("Speed Increased")
    elif key== GLUT_KEY_DOWN:
        speed /= 2
        print("Speed Decreased")
    for i in points:
        if i.x_speed != 0:
            i.x_speed = speed if i.x_speed > 0 else -speed
        if i.y_speed != 0:
            i.y_speed = speed if i.y_speed > 0 else -speed
    glutPostRedisplay()

def animate():
    if not pause:
        for i in points:
            i.x += i.x_speed
            i.y += i.y_speed

            if i.x>1.0:
                i.x=1.0
                i.x_speed=-abs(i.x_speed)
            elif i.x<-1.0:
                i.x=-1.0
                i.x_speed=abs(i.x_speed)

            if i.y>1.0:
                i.y=1.0
                i.y_speed=-abs(i.y_speed)
            elif i.y<-1.0:
                i.y=-1.0
                i.y_speed=abs(i.y_speed)
    glutPostRedisplay()



def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    draw_points()
    glutSwapBuffers()

def init():
    glClearColor(0,0,0,0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, W_Width, W_Height, 0.0, 0.0, 1)



glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) #	//Depth, Double buffer, RGB color
glutCreateWindow(b"task2")
init()

glutDisplayFunc(display)	#display callback function
#glutIdleFunc(animate)	#what you want to do in the idle time (when no drawing is occuring)

#glutKeyboardFunc(keyboard_connection)
#glutSpecialFunc(arrow_Key_connection)
glutMouseFunc(mouse_connection)

glutMainLoop()	