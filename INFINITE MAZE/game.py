
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math, random


# Camera-related variables
camera_pos = (0, 500, 500)

fovY = 120  # Field of view
GRID_LENGTH = 800  # Length of grid lines
rand_var = 423

maze_wall= [[-800, 800, 800, 800],
            [-800, -800, 800, -800],
            [-800, -670, -800, 800],
            [800, -800, 800, 670],
            [800, 300, -280, 300],
            [-280, 300, -280, 550],
            [-450, 450, -800, 450],
            [-200, 800, -200, 650],
            [-200, 800, -200, 650],
            [-200, 650, -500, 650],
            [10, 800, 10, 450],
            [210, 300, 210, 650],
            [410, 800, 410, 450],
            [410, 450, 640, 450],
            [800, 670, 640, 670],
            [410, -800, 410, -250],
            [410, -250, 620, -250],
            [620, -550, 620, 70],
            [420, 70, 170, 70],
            [170, 70, 170, -550],
            [170, -550, -250, -550],
            [-30, 300, -30, -250],
            [-250, -550, -250, 70],
            [-250, 70, -550, 70],
            [-550, 70, -500, 320],
            [-800, -250, -250, -250],
            [-550, -800, -550, -500]]


# man
man = {
    "head" : {"create": [20, 10, 10], 
              "color": (0.0, 1.0, 1.0), 
              "position": [50, 400, 80]},
    
    "body" : {"create": [30, 30, 50], 
              "color" : (0.04, 0.47, 0.19), 
              "position" :[50, 400, 80-20-25]},
    
    "legs" : [{"create_base": 10, 
               "create_top": 2,            # right
               "height": 40,
               "color":(0, 0, 0),
               "position" : [50 + 8, 400, 45 - 15 - 10] },

              {"create_base": 10, 
               "create_top": 2,                # left
               "height": 40,
               "color":(0, 0, 0),
               "position" : [50 - 8, 400, 45 - 15 - 10] }],


    "arms" : [{"create_base": 5,
               "create_top": 2,
               "height": 40,
               "color": (0, 0, 0),
               "position" : [50 + 20 , 400, 45] ,  
               "rotation": [90, 1, 0, 0] },

              { "create_base": 5,
                "create_top": 2,
                "height": 40,
                "color": (0, 0, 0),
                "position" : [50 - 20, 400, 45] ,
                "rotation": [90, 1, 0, 0]}],


    

    "theta" : math.radians(0),  # for movement direction
    "rot_theta" : 0, # angle of rotation about z-axis
} 

#game stat
game_r = True

#game elements
tele_cor = [(590, 710), (440, 180), (-315, 430), (320, 650), (660, 90), (90, 380), (100, 720), (-390, 320)]
tele_dis = 100 
tele_update = True
tele_i1 = None 
tele_i2 = None

def draw_man():
    global man
    
    #rotate as a whole
    glPushMatrix()
    body_pos = man["body"]["position"]
    center = body_pos[2] - (man["body"]["create"][2] / 2)  # base center of the cube
    
    glTranslatef(body_pos[0], body_pos[1], center)
    glRotatef(man["rot_theta"], 0, 0, 1)
    glTranslatef(-body_pos[0], -body_pos[1], -center)
    #arms 

    #right
    glPushMatrix()
    r, g, b = man['arms'][0]['color']
    pos = man["arms"][0]["position"]
    glTranslatef(pos[0], pos[1], pos[2])
    rot = man["arms"][0]["rotation"] 
    glRotatef(rot[0], rot[1], rot[2], rot[3])
    glColor3f(r,g,b)
    l = man["arms"][0]
    gluCylinder(gluNewQuadric(),   l["create_base"], l["create_top"], l["height"], 10, 10 )  
    glPopMatrix()


    #left
    glPushMatrix()
    r, g, b = man['arms'][1]['color']
    pos = man["arms"][1]["position"]
    rot = man["arms"][1]["rotation"] 
    glTranslatef(pos[0], pos[1], pos[2]) 
    glRotatef(rot[0], rot[1], rot[2], rot[3])
    glColor3f(r,g,b)
    l = man["arms"][1]
    gluCylinder(gluNewQuadric(),  l["create_base"], l["create_top"], l["height"], 10, 10 )  
    glPopMatrix()





    #legs 

    #right
    glPushMatrix()
    r, g, b = man['legs'][0]['color']
    pos = man["legs"][0]["position"]
    glTranslatef(pos[0], pos[1], pos[2]) 
    glRotatef(-180, 1, 0, 0)
    glColor3f(r,g,b)
    l = man["legs"][0]
    gluCylinder(gluNewQuadric(),   l["create_base"], l["create_top"], l["height"], 10, 10 )  
    glPopMatrix()


    #left
    glPushMatrix()
    r, g, b = man['legs'][1]['color']
    pos = man["legs"][1]["position"]
    glTranslatef(pos[0], pos[1], pos[2]) 
    glRotatef(-180, 1, 0, 0)
    glColor3f(r,g,b)
    l = man["legs"][1]
    gluCylinder(gluNewQuadric(),  l["create_base"], l["create_top"], l["height"], 10, 10 )  
    glPopMatrix()


    
    



    # body drawing
    glPushMatrix()
    size = man["body"]["create"][0]
    r, g, b = man['body']['color']
    pos = man["body"]
    glTranslatef(*pos["position"])
    glScalef(1, 1, 5/3) 
    glColor3f(r,g,b)
    glutSolidCube(size) 
    glPopMatrix()


    # head drawing
    glPushMatrix()
    r, g, b = man["head"]["color"]
    glColor3f(r,g,b)
    pos = man["head"]["position"]
    glTranslatef(pos[0], pos[1], pos[2])
    r,s,st = man["head"]["create"]
    gluSphere(gluNewQuadric(), r, s, st)
    glPopMatrix()
    glPopMatrix()

def spawn():
    x = random.uniform()


def draw_maze():
    glPushMatrix()
    glColor3f(0, 0, 1)  # Maze wall color (white)

    wall_thickness = 10
    wall_height = 80

    # Outer rectangle walls (top, bottom, left, right)
    def draw_wall(x1, y1, x2, y2):
        glBegin(GL_QUADS)
        glVertex3f(x1, y1, 0)
        glVertex3f(x2, y2, 0)
        glVertex3f(x2, y2, wall_height)
        glVertex3f(x1, y1, wall_height)
        glEnd()

    # Outer boundaries
    draw_wall(maze_wall[0][0],maze_wall[0][1],maze_wall[0][2], maze_wall[0][3])    # Top wall
    draw_wall(maze_wall[1][0],maze_wall[1][1],maze_wall[1][2],maze_wall[1][3])  # Bottom wall
    draw_wall(maze_wall[2][0],maze_wall[2][1],maze_wall[2][2],maze_wall[2][3])  # r8 wall
    draw_wall(maze_wall[3][0], maze_wall[3][1],maze_wall[3][2],maze_wall[3][3])    # left wall

    # Maze internal walls(lower)
    draw_wall(maze_wall[4][0], maze_wall[4][1],maze_wall[4][2], maze_wall[4][3])
    draw_wall(maze_wall[5][0], maze_wall[5][1],maze_wall[5][2], maze_wall[5][3])
    draw_wall(maze_wall[6][0],maze_wall[6][1],maze_wall[6][2], maze_wall[6][3])
    draw_wall(maze_wall[7][0], maze_wall[7][1], maze_wall[7][2], maze_wall[7][3])
    draw_wall(maze_wall[8][0],maze_wall[8][1],maze_wall[8][2],maze_wall[8][3])
    draw_wall(maze_wall[9][0], maze_wall[9][1],maze_wall[9][2],maze_wall[9][3])
    draw_wall(maze_wall[10][0], maze_wall[10][1],maze_wall[10][2],maze_wall[10][3])
    draw_wall(maze_wall[11][0],maze_wall[11][1],maze_wall[11][2],maze_wall[11][3])
    draw_wall(maze_wall[12][0],maze_wall[12][1],maze_wall[12][2],maze_wall[12][3])
    draw_wall(maze_wall[13][0],maze_wall[13][1],maze_wall[13][2],maze_wall[13][3])
    draw_wall(maze_wall[14][0],maze_wall[14][1],maze_wall[14][2],maze_wall[14][3])


    #(upper walls)
    draw_wall(maze_wall[15][0],maze_wall[15][1],maze_wall[15][2],maze_wall[15][3])
    draw_wall(maze_wall[16][0],maze_wall[16][1],maze_wall[16][2],maze_wall[16][3])
    draw_wall(maze_wall[17][0],maze_wall[17][1],maze_wall[17][2],maze_wall[17][3])
    draw_wall(maze_wall[18][0],maze_wall[18][1],maze_wall[18][2],maze_wall[18][3])
    draw_wall(maze_wall[19][0],maze_wall[19][1],maze_wall[19][2],maze_wall[19][3])
    draw_wall(maze_wall[20][0],maze_wall[20][1],maze_wall[20][2],maze_wall[20][3])

    draw_wall(maze_wall[21][0],maze_wall[21][1],maze_wall[21][2],maze_wall[21][3])

    draw_wall(maze_wall[22][0],maze_wall[22][1],maze_wall[22][2],maze_wall[22][3])
    draw_wall(maze_wall[23][0],maze_wall[23][1],maze_wall[23][2],maze_wall[23][3])
    draw_wall(maze_wall[24][0],maze_wall[24][1],maze_wall[24][2],maze_wall[24][3])

    draw_wall(maze_wall[25][0],maze_wall[25][1],maze_wall[25][2],maze_wall[25][3])
    draw_wall(maze_wall[26][0],maze_wall[26][1],maze_wall[26][2],maze_wall[26][3])



    glPopMatrix()


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    # # Move forward (W key)
    # if key == b'w':

    # # Move backward (S key)
    # if key == b's':

    # # Rotate gun left (A key)
    # if key == b'a':

    # # Rotate gun right (D key)
    # if key == b'd':

    # # Toggle cheat mode (C key)
    # if key == b'c':

    # # Toggle cheat vision (V key)
    # if key == b'v':

    # # Reset the game if R key is pressed
    # if key == b'r':


def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos
    x, y, z = camera_pos
    # Move camera up (UP arrow key)
    if key == GLUT_KEY_UP:
        z += 1

    # # Move camera down (DOWN arrow key)
    if key == GLUT_KEY_DOWN:
        z -= 1

    # moving camera left (LEFT arrow key)
    if key == GLUT_KEY_LEFT:
        x -= 1  # Small angle decrement for smooth movement

    # moving camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        x += 1  # Small angle increment for smooth movement

    camera_pos = (x, y, z)


def mouseListener(button, state, x, y):
    print(x, y)
    # # Left mouse button fires a bullet
    # if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:

    # # Right mouse button toggles camera tracking mode
    # if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:


def setupCamera():
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, 1.25, 0.1, 1500)  # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix

    # Extract camera position and look-at target
    x, y, z = camera_pos
    # Position the camera and set its orientation
    gluLookAt(x, y, z,  # Camera position
              0, 0, 0,  # Look-at target
              0, 0, 1)  # Up vector (z-axis)

def draw_teleport(x1,y1, x2,y2):
    
    glPushMatrix()
    pos = (x1, y1, 1)
    glTranslatef(pos[0], pos[1], pos[2]) 
    
    glColor3f(1,0,0)
    gluCylinder(gluNewQuadric(), 70  , 70 , 10 , 10, 10 ) 

    glColor3f(0,1,0)
    gluCylinder(gluNewQuadric(), 50  , 50 , 20 , 10, 10 )  

    glColor3f(0,0,1)
    gluCylinder(gluNewQuadric(), 30  , 30 , 30 , 10, 10 )  
    glPopMatrix()





    glPushMatrix()
    pos = (x2, y2, 1)
    glTranslatef(pos[0], pos[1], pos[2])

    glColor3f(1,0,0)
    gluCylinder(gluNewQuadric(), 70  , 70 , 10 , 10, 10  )  

    glColor3f(0,1,0)
    gluCylinder(gluNewQuadric(), 50  , 50 , 20 , 10, 10 )

    glColor3f(0,0,1)
    gluCylinder(gluNewQuadric(), 30  , 30 , 30 , 10, 10 )  
    glPopMatrix()
def teleport():
    global tele_i1, tele_i2, tele_update, tele_dis
    
    if tele_update:
        tele_i1 = random.randint(0, len(tele_cor)-1)
        tele_i2 = random.randint(0, len(tele_cor)-1)
        if tele_i1 == tele_i2:
            tele_i2 = random.randint(0, len(tele_cor)-1)
        
        tele_update = False
    draw_teleport(tele_cor[tele_i1][0], tele_cor[tele_i1][1], tele_cor[tele_i2][0], tele_cor[tele_i2][1])


    temp1 = math.pow(math.pow(man["head"]["position"][0] - tele_cor[tele_i1][0], 2) + math.pow(man["head"]["position"][1] - tele_cor[tele_i1][1], 2) , 0.5)
    temp2 = math.pow(math.pow(man["head"]["position"][0] - tele_cor[tele_i2][0], 2) + math.pow(man["head"]["position"][1] - tele_cor[tele_i2][1], 2) , 0.5)
    if temp1 > temp2:
            tele_dis = temp2
    else:
            tele_dis = temp1
    

def idle():
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """    
    # Ensure the screen updates with the latest changes

    
    
    glutPostRedisplay()


def showScreen():
    global game_r
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 800)  # Set viewport size

    setupCamera()  # Configure camera perspective

    # Draw a random points
    glPointSize(20)
    glBegin(GL_POINTS)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glEnd()

    # Draw the grid (game floor)
    glBegin(GL_QUADS)

    glColor3f(1, 1, 1)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(0, GRID_LENGTH, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(-GRID_LENGTH, 0, 0)

    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(0, -GRID_LENGTH, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(GRID_LENGTH, 0, 0)

    glColor3f(0.7, 0.5, 0.95)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, -GRID_LENGTH, 0)

    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, GRID_LENGTH, 0)
    glEnd()

    # Display game info text at a fixed screen position
    draw_text(10, 770, f"A Random Fixed Position Text")
    draw_text(10, 740, f"See how the position and variable change?: {rand_var}")


    if game_r:
        game_r = False
        tele_update = True
    
    teleport()

    draw_man()
    
    draw_maze()

    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()


# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"3D OpenGL Intro")  # Create the window

    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically

    glutMainLoop()  # Enter the GLUT main loop


if __name__ == "__main__":
    main()
