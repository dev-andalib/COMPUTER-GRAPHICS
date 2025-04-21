from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

fovY = 150
grid_length = 50

man = [
    ["head", [20, 10, 10], (0.0, 1.0, 1.0), [50, 320, 80]],
    ["body", [30, 30, 50], (0.04, 0.47, 0.19), [50, 320, 35]],
    ["legs", [
        [10, 2, 40, (0, 0, 0), [58, 320, 20]],
        [10, 2, 40, (0, 0, 0), [42, 320, 20]]
    ]],
    ["arms", []],
    ["gun", []]
]

camera_pos = [50, -200, 100]
camera_center = [50, 320, 50]
step_size = random.randint(1, 10)

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    pass

def draw_shapes():
    pass

def keyboardListener(key, x, y):
    global camera_pos, step_size
    z = camera_pos[2]
    if key == b'w': z += step_size
    if key == b's': z -= step_size
    camera_pos[2] = z

def specialKeyListener(key, x, y):
    global camera_pos, step_size
    x, y, z = camera_pos
    if key == GLUT_KEY_DOWN: y -= step_size
    elif key == GLUT_KEY_UP: y += step_size
    elif key == GLUT_KEY_LEFT: x += step_size
    elif key == GLUT_KEY_RIGHT: x -= step_size
    camera_pos = [x, y, z]

def mouseListener(button, state, x, y):
    print(x, y)

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(*camera_pos, *camera_center, 0, 0, 1)

def idle():
    glutPostRedisplay()

def draw_tile(x, y):
    start = [x, y]
    glVertex3f(start[0], start[1], 0)
    glVertex3f(start[0]+grid_length, start[1], 0)
    glVertex3f(start[0]+grid_length, start[1]+grid_length, 0)
    glVertex3f(start[0], start[1]+grid_length, 0)

def draw_boundary(i, cor):
    glBegin(GL_QUADS)
    colors = [(1.0,0.0,0.0), (0.0,1.0,0.0), (0.0,0.0,1.0), (1.0,1.0,0.0)]
    glColor3f(*colors[i])
    for j in range(len(cor)):
        x, y, z = cor[j]
        glVertex3f(x, y, z)
    glEnd()

def draw_man():
    body_parts = random.sample(man[:3], 3)
    for part in body_parts:
        if part[0] == "head":
            glPushMatrix()
            glColor3f(*part[2])
            glTranslatef(*part[3])
            gluSphere(gluNewQuadric(), part[1][0], part[1][1], part[1][2])
            glPopMatrix()
        elif part[0] == "body":
            glPushMatrix()
            glColor3f(*part[2])
            glTranslatef(*part[3])
            glScalef(1, 1, part[1][2]/part[1][0])
            glutSolidCube(part[1][0])
            glPopMatrix()
        elif part[0] == "legs":
            for leg in part[1]:
                glPushMatrix()
                glColor3f(*leg[3])
                glTranslatef(*leg[4])
                glRotatef(-180, 1, 0, 0)
                gluCylinder(gluNewQuadric(), leg[0], leg[1], leg[2], 10, 10)
                glPopMatrix()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    setupCamera()
    
    start = [-275,-9]
    temp = start.copy()
    for i in range(13):
        for j in range(13):
            glBegin(GL_QUADS)
            glColor3f(1,1,1) if (i+j)%2==0 else glColor3f(0.7,0.5,0.95)
            draw_tile(start[0], start[1])
            glEnd()
            start[0] += 50
        start[1] += grid_length
        start[0] = temp[0]
    
    h_max, h_min = 100, 0
    x_max, x_min = 375, -275
    y_max, y_min = 640, -9
    boundary = [
        [[x_min,y_min,h_min],[x_min,y_min,h_max],[x_max,y_min,h_max],[x_max,y_min,h_min]],
        [[x_min,y_min,h_min],[x_min,y_min,h_max],[x_min,y_max,h_max],[x_min,y_max,h_min]],
        [[x_max,y_min,h_min],[x_max,y_min,h_max],[x_max,y_max,h_max],[x_max,y_max,h_min]],
        [[x_min,y_max,h_min],[x_min,y_max,h_max],[x_max,y_max,h_max],[x_max,y_max,h_min]]
    ]
    for i in range(4):
        draw_boundary(i, boundary[i])
    
    draw_man()
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 680)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"SHOOT ENEMIES")
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()