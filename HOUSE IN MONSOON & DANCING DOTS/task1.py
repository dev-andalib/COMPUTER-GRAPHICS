# TASK 1
#################################################################
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random, math, time


background = {
    "land":[
        [(-1,1/2),(-1,-1),(1,-1),(-1,1/2),(1,1/2),(1,-1)],
        (88/255, 57/255, 39/255)
    ],

    "sky":[
        [(-1,1),(-1, 1/2),(1,1/2),(-1, 1), (1,1/2), (1,1)],
        (0,0,0),
    ],
    "house":{
        'roof' : [
            [(-.49, 0.44), (0, 0.7), (0.49, 0.44)],
            (115/255, 147/255, 179/255),
        ],
        'base' : [
            [(-.39, 0.44), (-.39, 0.14), (0.39, 0.14), (-.39, 0.44), (0.39, 0.44), (0.39, 0.14)],
            (245/255, 245/255, 245/255)
        ],
        'window': [
            [(-.29, 0.34), (-.29, 0.24), (-.19, 0.34), (-.19, 0.34), (-0.19, 0.24), (-0.29, 0.24)],
            [(.29, 0.34), (.29, 0.24), (.19, 0.34), (.19, 0.34), (0.19, 0.24), (0.29, 0.24)],
            (135/255, 206/255, 235/255)
        ],
        'door' : [
            [(-.09, 0.34), (-.09, 0.14), (0.09, 0.34), (-.09, 0.14), (.09, 0.34), (0.09, 0.14)],
            (54/255, 34/255, 4/255)
        ]
    },


}

dayandnight = {
    "color": [0, 42, 127, 212, 255],
    "dayornight" : 'night'
               }


rain = {
    "point": [],
    "color": [(20/255,20/255,20/255),
    (240/255,240/255,240/255),
    (173/255,216/255,230/255),
    (0,0,139/255)],
    "angle" : 0,
}


W_Width = 1000
W_Height = 700


def convert_coordinate(x,y):
    global W_Width, W_Height
    x_cor = (2*x - W_Width)/W_Width
    y_cor = (W_Height - 2*y)/W_Height
    return (x_cor, y_cor)



def letsDraw():
    global  background, rain
    glPointSize(2)
    glBegin(GL_TRIANGLES)

    #DRAWING SKY
    skyCol = background['sky'][1]
    a,b,c = skyCol
    glColor3f(a, b, c)

    for i in background['sky'][0]:
        x, y = i
        glVertex2d(x,y)

    #DRAWING LAND
    landCol = background['land'][1]
    a, b, c = landCol
    glColor3f(a, b, c)
    for i in background['land'][0]:
        x, y = i
        glVertex2d(x,y)


    #DRAWING house
    #ROOF
    roofCol = background['house']["roof"][1]
    a, b, c = roofCol
    glColor3f(a, b, c)
    for i in background['house']["roof"][0]:
        x, y = i
        glVertex2d(x, y)

    #BASE OF HOUSE
    baseCol = background['house']["base"][1]
    a, b, c = baseCol
    glColor3f(a, b, c)
    for i in background['house']["base"][0]:
        x, y = i
        glVertex2d(x, y)

    # window
    winCol = background['house']["window"][2]
    a, b, c = winCol
    glColor3f(a, b, c)
    for i in background['house']["window"][0]:
        x, y = i
        glVertex2d(x, y)

    for i in background['house']["window"][1]:
        x, y = i
        glVertex2d(x, y)

    # door
    doorCol = background['house']["door"][1]
    a, b, c = doorCol
    glColor3f(a, b, c)
    for i in background['house']["door"][0]:
        x, y = i
        glVertex2d(x, y)

    glEnd()

    glPointSize(1)
    glBegin(GL_LINES)
    for i in rain['point']:
        x = i[0]
        y = i[1]
        rainH = i[2]
        a, b, c = rain['color'][random.randint(0,3)]
        glColor3f(a,b,c)

        glVertex2d(x,y)
        y -= rainH
        x += rainH* math.sin(rain["angle"])
        glVertex2d(x,y)

    glEnd()


def movement():
    global rain
    for i in rain['point']:
        y = i[1]
        if y >= -0.8:
            i[1]  -= i[2] * math.cos(rain['angle'])
            i[0] += i[2] * math.sin(rain["angle"])
        else:
            rain['point'] = []
            createRain()

    glutPostRedisplay()


def windEffect(key, x, y):
    global rain
    print(rain['angle'])
    if key == GLUT_KEY_LEFT and rain["angle"] >= -1 *  math.pi/8:
        rain["angle"] -= math.pi/8
    elif key == GLUT_KEY_RIGHT and rain["angle"] <=  math.pi/8:
        rain["angle"] += math.pi/8

def delay1(i):
    background['sky'][1] = (
    dayandnight['color'][i] / 255, dayandnight['color'][i] / 255, dayandnight['color'][i] / 255)
    glutPostRedisplay()

def delay2(i):
    background['sky'][1] = (dayandnight['color'][i] / 255, dayandnight['color'][i] / 255, dayandnight['color'][i] / 255)
    glutPostRedisplay()

def dayNight(key,x, y):
    global  background, dayandnight

    if key == b'w' and dayandnight['dayornight'] == 'night':
        dayandnight['dayornight'] = "day"
        for i in range(len(dayandnight['color'])):
            glutTimerFunc(500*i, delay1, i)



    elif key == b's'  and dayandnight['dayornight'] == 'day':
        dayandnight['dayornight'] = "night"
        for i in reversed(range(len(dayandnight['color']))):
            time = len(dayandnight['color']) - i
            glutTimerFunc(500 * time, delay1, i)




def createRain():
    global rain
    for i in range(500):
        x = random.uniform(-4, 4)
        y = 1
        rainH = random.uniform(0.01, 0.1)
        rain["point"].append([x,y, rainH])

def showStuff():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    letsDraw()
    glutSwapBuffers()


def start():
    glClearColor(1, 1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1, 1, -1, 1)
    createRain()





glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"TASK 1")


start()


glutDisplayFunc(showStuff)
glutIdleFunc(movement)
glutSpecialFunc(windEffect)
glutKeyboardFunc(dayNight)

glutMainLoop()