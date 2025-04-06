import random
from calendar import firstweekday
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math



W_Width, W_Height = 400, 700
diamond = None
catcher = None
score = 0
Game_On = True
Diamond_caught = False

class Diamond:
    size = 0.02
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.points = [[self.x, self.y],
                       [self.x+1.5*Diamond.size, self.y-3*Diamond.size], 
                       [self.x, self.y-6*Diamond.size], 
                       [self.x-1.5*Diamond.size, self.y-3*Diamond.size]]
        self.color = (random.uniform(0,1),random.uniform(0,1), random.uniform(0,1))

    def setPoints(self, x, y):
        self.x = x
        self.y = y
        self.points = [[self.x, self.y],
                       [self.x+1.5*Diamond.size, self.y-3*Diamond.size], 
                       [self.x, self.y-6*Diamond.size], 
                       [self.x-1.5*Diamond.size, self.y-3*Diamond.size]]


class Catcher:
    size = 0.1
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.points = [[self.x, self.y],
                       [self.x + 5*Catcher.size, self.y],
                       [self.x+0.1 + 3 * Catcher.size, self.y - 0.5*Catcher.size],
                       [self.x+0.1, self.y -  0.5*Catcher.size]
                       ]
        self.color = (1,1,1)

    def setPoints(self, x, y):
        self.x = x
        self.y = y
        self.points = [[self.x, self.y],
                       [self.x + 5*Catcher.size, self.y],
                       [self.x+0.1 + 3 * Catcher.size, self.y - 0.5*Catcher.size],
                       [self.x+0.1, self.y -  0.5*Catcher.size]
                       ]



def convert_coordinate(x,y):
    global W_Width, W_Height
    x_cor = (2*x - W_Width)/W_Width
    y_cor = (W_Height - 2*y)/W_Height
    return [x_cor, y_cor]

def midpoint_line_draw(p1, p2):

    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    zone = None
    quadrant = None

    # find quadrant
    if dx > 0:
        if dy > 0:
            quadrant = 'first'
        else:
            quadrant = 'forth'
    elif dx < 0:
        if dy > 0:
            quadrant = 'second'
        else:
            quadrant = 'third'


    #find zone
    if quadrant == 'first':
        if abs(dx) > abs(dy):
            zone = 0
        else:
            zone = 1

    elif quadrant == 'forth':
        if abs(dx) > abs(dy):
            zone = 7
        else:
            zone = 6

    elif quadrant == 'second':
        if abs(dx) > abs(dy):
            zone = 3
        else:
            zone = 2

    elif quadrant == 'third':
        if abs(dx) > abs(dy):
            zone = 4
        else:
            zone = 5

    # adjustment based on zone
    p1, p2 = zone_adjust(p1, p2, zone)
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]

    d = 2 * dy - dx
    inc = 0.0001

    point_list = [p1]

    while p1[0] < p2[0]:
        if d > 0: #NE
            d = d + 2*dy - 2*dx
            p1[0] += inc
            p1[1] += inc

        else:
            d = d + 2*dy
            p1[0] += inc
        point_list.append([p1[0], p1[1]])

    for i in range(len(point_list)):
        point_list[i] = zone_readjust(point_list[i], zone)

    return point_list

def zone_readjust(p1, zone):
    if zone == 1:
        return [p1[1], p1[0]]
    elif zone == 2:
        x, y = zone_readjust(p1, 1)
        return [-x, y]
    elif zone == 3:
        return [-p1[0], p1[1]]
    elif zone == 4:
        x, y = zone_readjust(p1, 7)
        return [-x, y]
    elif zone == 5:
        x, y = zone_readjust(p1, 6)
        return [-x, y]
    elif zone == 6:
        x, y = zone_readjust(p1, 7)
        return [-y, -x]
    elif zone == 7:
        return [p1[0], -p1[1]]
    return p1

def zone_adjust(p1, p2, zone):
    if zone == 1:
        return [p1[1], p1[0]], [p2[1], p2[0]]
    elif zone == 2:
        p1, p2 = zone_adjust([-p1[0], p1[1]], [-p2[0], p2[1]], 1)
        return p1, p2
    elif zone == 3:
        return [-p1[0], p1[1]], [-p2[0], p2[1]]
    elif zone == 4:
        p1, p2 = zone_adjust([p1[0], -p1[1]], [p2[0], -p2[1]], 3)
        return p1, p2
    elif zone == 5:
        p1, p2 = zone_adjust([p1[0], -p1[1]], [p2[0], -p2[1]], 2)
        return p1, p2
    elif zone == 6:
        p1, p2 = zone_adjust([-p1[0], p1[1]], [-p2[0], p2[1]], 5)
        return p1, p2
    elif zone == 7:
        return [p1[0], -p1[1]], [p2[0], -p2[1]]
    return p1, p2


def draw(p1, p2, obj1):

    line = midpoint_line_draw(p1,p2)
    glPointSize(2)
    a, b, c = obj1.color
    glBegin(GL_POINTS)
    glColor3f(a,b,c)
    for i in line:
        glVertex2d(i[0], i[1])
    glEnd()

def diamond_fall():
    global diamond, catcher
    d1 = diamond
    c1 = catcher
    step_size = 0.008
    if d1.points[3][1] >=  -0.80:
        d1.setPoints(d1.x, d1.y-step_size)
    
    else:
        d1.setPoints(random.uniform(-0.75,0.75), 0.75)
        Diamond_caught = False
    glutPostRedisplay() 


def catcher_move(key, x, y):
    global catcher
    c1 = catcher
    step_size = 0.08
    if key == GLUT_KEY_LEFT and c1.x > -1:
        c1.setPoints(c1.x - step_size, c1.y)
    elif key == GLUT_KEY_RIGHT and c1.x+0.5 < 1:
        c1.setPoints(c1.x + step_size, c1.y)
    glutPostRedisplay() 

def draw_shape(obj):
    for i in range(len(obj.points)):
        draw(obj.points[i%len(obj.points)], obj.points[(i+1)%len(obj.points)], obj)
       

def game_init():
    global diamond, catcher
    diamond = Diamond(random.uniform(-0.75,0.75), 0.75)
    catcher = Catcher(random.uniform(-1, 0.5), -0.85)



def showStuff():
    global diamond, catcher, score, Game_On, Diamond_caught
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    draw_shape(diamond)
    draw_shape(catcher)
    d1 = diamond
    c1 = catcher
    if not Diamond_caught and d1.points[2][1] <= c1.y:
        if d1.points[2][0] <= c1.points[0][0] or d1.points[2][0] > c1.points[1][0]:
            Game_On = False
            print(Game_On)
        
        else:
            score += 1
            print(score)
            print(Game_On)
    
        Diamond_caught = True
    glutSwapBuffers()


def start():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1, 1, -1, 1)
    game_init()





glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"CATCH THE DIAMOND")

start()

glutDisplayFunc(showStuff)
glutIdleFunc(diamond_fall)
glutSpecialFunc(catcher_move)
# glutKeyboardFunc(dayNight)
glutMainLoop()