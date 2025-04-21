import copy
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random


fovY = 150  # How wide the camera can see in vertical direction
grid_length = 50  # Length of grid lines


#game stat
stat = "restarted"

#man object
man = {
    "head" : {"create": [20, 10, 10], 
              "color": (0.0, 1.0, 1.0), 
              "position": [50, 320, 80]},
    
    "body" : {"create": [30, 30, 50], 
              "color" : (0.04, 0.47, 0.19), 
              "position" :[50, 320, 80-20-25]},
    
    "legs" : [{"create_base": 10, 
               "create_top": 2,            # right
               "height": 40,
               "color":(0, 0, 0),
               "position" : [50 + 8, 320, 45 - 15 - 10] },

              {"create_base": 10, 
               "create_top": 2,                # left
               "height": 40,
               "color":(0, 0, 0),
               "position" : [50 - 8, 320, 45 - 15 - 10] }],


    "arms" : [{"create_base": 5,
               "create_top": 2,
               "height": 40,
               "color": (0, 0, 0),
               "position" : [50 + 20 , 320, 45] ,  
               "rotation": [90, 1, 0, 0] },

              { "create_base": 5,
                "create_top": 2,
                "height": 40,
                "color": (0, 0, 0),
                "position" : [50 - 20, 320, 45] ,
                "rotation": [90, 1, 0, 0]}],


    "gun"  : {"create_base": 5,
               "create_top": 5,
               "height": 60,
               "color": (0.251, 0.251, 0.251),
               "position" : [50 , 310, 45] ,  
               "rotation": [90, 1, 0, 0] },
}

# enemy object


enemy = {
    "head" : {"create": [20, 10, 10], 
              "color": (0.251, 0.251, 0.251), 
              "position": [50, 320, 80]},


    "body" : {"create": [50, 100, 100], 
              "color": (1, 0, 0), 
              "position": [50, 320, 80-20-25]},
}

enemy_list = []


#camera position
camera_pos = [50, -200, 100] 
camera_center = [50, 320, 50] 
step_size = 5

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    pass
    # glColor3f(1,1,1)
    # glMatrixMode(GL_PROJECTION)
    # glPushMatrix()
    # glLoadIdentity()
    
    # # Set up an orthographic projection that matches window coordinates
    # gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

    
    # glMatrixMode(GL_MODELVIEW)
    # glPushMatrix()
    # glLoadIdentity()
    
    # # Draw text at (x, y) in screen coordinates
    # glRasterPos2f(x, y)
    # for ch in text:
    #     glutBitmapCharacter(font, ord(ch))
    
    # # Restore original projection and modelview matrices
    # glPopMatrix()
    # glMatrixMode(GL_PROJECTION)
    # glPopMatrix()
    # glMatrixMode(GL_MODELVIEW)


def draw_shapes():
    pass
    # glPushMatrix()  # Save the current matrix state
    
    # glColor3f(1, 0, 0)
    # glTranslatef(0, 0, 0)  
    # glutSolidCube(60) # Take cube size as the parameter
    # glTranslatef(0, 0, 100) 
    # glColor3f(0, 1, 0)
    # glutSolidCube(60) 

    # glColor3f(1, 1, 0)
    # gluCylinder(gluNewQuadric(), 40, 5, 150, 10, 10)  # parameters are: quadric, base radius, top radius, height, slices, stacks
    # glTranslatef(100, 0, 100) 
    # glRotatef(90, 0, 1, 0)  # parameters are: angle, x, y, z
    # gluCylinder(gluNewQuadric(), 40, 5, 150, 10, 10)

    # glColor3f(0, 1, 1)
    # glTranslatef(300, 0, 100) 
    # gluSphere(gluNewQuadric(), 80, 10, 10)  # parameters are: quadric, radius, slices, stacks

    # glPopMatrix()  # Restore the previous matrix state


def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """

    global camera_pos, step_size
    
    z = camera_pos[2]
    
    # Move forward (W key)
    if key == b'w':  
       z += step_size 

    # Move backward (S key)
    if key == b's':
       z -= step_size

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
    camera_pos[2] = z

def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos, step_size
    x = camera_pos[0]
    y = camera_pos[1]
    z = camera_pos[2]
    
    if key == GLUT_KEY_DOWN:
        y -= step_size
    
    elif key == GLUT_KEY_UP:
        y += step_size
    
    elif key == GLUT_KEY_LEFT:
        x += step_size 

    
    elif key == GLUT_KEY_RIGHT:
        x -= step_size  
    
    camera_pos.clear()
    camera_pos = [x, y, z]
    


def mouseListener(button, state, x, y):
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
        # # Left mouse button fires a bullet
        # if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:

        # # Right mouse button toggles camera tracking mode
        # if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
    print(x, y)

def setupCamera():
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    glMatrixMode(GL_PROJECTION) 
    glLoadIdentity() # reset matrix
                         # aspect ration (W/H), object 
                         # closer than 0.1 are not visible
                         # farther than 1500 are not visible
    gluPerspective(fovY, 1.25, 0.1, 1500) 

    glMatrixMode(GL_MODELVIEW) # move or rotate object  
    glLoadIdentity()  

   
    global camera_pos, camera_center 
    x = camera_pos[0]
    y = camera_pos[1]
    z = camera_pos[2]


    x1 = camera_center[0]
    y1 = camera_center[1]
    z1 = camera_center[2]
    
    gluLookAt(x, y, z,  
              x1, y1, z1,  
              0, 0, 1)  


def idle():
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    # Ensure the screen updates with the latest changes
    glutPostRedisplay()

def draw_tile(x, y):
    start = [x, y]
    glVertex3f(start[0], start[1], 0)
    glVertex3f(start[0]+grid_length, start[1], 0)
    glVertex3f(start[0]+grid_length, start[1]+grid_length, 0)
    glVertex3f(start[0], start[1]+grid_length, 0)

def draw_boundary(i, cor):
    glBegin(GL_QUADS)
    for j in range(len(cor)):
            if i == 0:
                color = (1.0, 0.0, 0.0)
                glColor3f(color[0], color[1], color[2])
                x = cor[j][0]
                y = cor[j][1]
                z = cor[j][2]    
                glVertex3f(x, y, z)
                
            
            elif i == 1:
                color = (0.0, 1.0, 0.0)
                glColor3f(color[0], color[1], color[2])
                x = cor[j][0]
                y = cor[j][1]
                z = cor[j][2]    
                glVertex3f(x, y, z)
               
            
            elif i == 2:
                color = (0.0, 0.0, 1.0)
                glColor3f(color[0], color[1], color[2])
                x = cor[j][0]
                y = cor[j][1]
                z = cor[j][2]    
                glVertex3f(x, y, z)
                
            
            elif i == 3:
                color = (1.0, 1.0, 0.0)
                glColor3f(color[0], color[1], color[2])
                x = cor[j][0]
                y = cor[j][1]
                z = cor[j][2]     
                glVertex3f(x, y, z)
                

    glEnd()

def draw_man():
    global man
    
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


    #gun
    glPushMatrix()
    r, g, b = man['gun']['color']
    pos = man["gun"]["position"]
    rot = man["gun"]["rotation"] 
    glTranslatef(pos[0], pos[1], pos[2]) 
    glRotatef(rot[0], rot[1], rot[2], rot[3])
    glColor3f(r,g,b)
    l = man["gun"]
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





def draw_enemy(i):
    enemy = i
    

    #bod
    glPushMatrix()
    r, g, b = enemy["body"]["color"]
    glColor3f(r,g,b)
    pos = enemy["body"]["position"]
    glTranslatef(pos[0], pos[1], pos[2])
    r,s,st = enemy["body"]["create"]
    gluSphere(gluNewQuadric(), r, s, st)
    glPopMatrix()

    #head
    glPushMatrix()
    r, g, b = enemy["head"]["color"]
    glColor3f(r,g,b)
    pos = enemy["head"]["position"]
    glTranslatef(pos[0], pos[1], pos[2])
    r,s,st = enemy["head"]["create"]
    gluSphere(gluNewQuadric(), r, s, st)
    glPopMatrix()
    return enemy






def enemy_creation(x_min, x_max, y_min, y_max):
    global enemy, enemy_list, stat
    
    
    for i in range(5):
        r = enemy["body"]["create"][0]

        x = random.uniform(x_min + r, x_max - r)
        y = random.uniform(y_min + r, y_max - r)

        enemy["body"]["position"][0] = x
        enemy["body"]["position"][1] = y

        enemy["head"]["position"][0] = x
        enemy["head"]["position"][1] = y

        enemy_list.append(copy.deepcopy(enemy))
        if i == 4:
            stat = "done"
           
            


def showScreen():
    global grid_length, enemy_list, stat
  
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)

    setupCamera()   
    
    
    
    # draw grids
    start = [-275,-9]
    temp = start.copy()
    for i in range(13):
        for j in range(13):
            if j%2 == 0 and i%2 == 0:
                glBegin(GL_QUADS)
                glColor3f(1, 1, 1)
                draw_tile(start[0], start[1])
                glEnd()
                start[0] += 50
            

            elif j%2 != 0 and i%2 == 0:
                glBegin(GL_QUADS)
                glColor3f(0.7, 0.5, 0.95)
                draw_tile(start[0], start[1])
                glEnd()
                start[0] += 50
            

            elif j%2 == 0 and i%2 != 0:
                glBegin(GL_QUADS)
                glColor3f(0.7, 0.5, 0.95)
                draw_tile(start[0], start[1])
                glEnd()
                start[0] += 50
            

            elif j%2 != 0 and i%2 != 0:
                glBegin(GL_QUADS)
                glColor3f(1,1,1)
                draw_tile(start[0], start[1])
                glEnd()
                start[0] += 50


        start[1] += grid_length
        start[0] = temp[0]     
   
    
    #boundary
    h_max = 100
    h_min = 0
    x_max = 375
    x_min = -275
    y_max = 640
    y_min = -9
    boundary = [
                 [[x_min,y_min, h_min],[x_min,y_min, h_max],[x_max, y_min, h_max],[x_max, y_min, h_min]], 
                 [[x_min,y_min, h_min],[x_min,y_min, h_max],[x_min, y_max, h_max],[x_min, y_max, h_min]], 
                 [[x_max,y_min, h_min],[x_max,y_min, h_max],[x_max, y_max, h_max],[x_max, y_max, h_min]], 
                 [[x_min,y_max, h_min],[x_min,y_max, h_max],[x_max, y_max, h_max],[x_max, y_max, h_min]]
               ]
    for i in range(len(boundary)):
        draw_boundary(i, boundary[i])
    
    
    #man
    # draw_man()


    #enemy
    if stat == "restarted":
        enemy_creation(x_min, x_max, y_min, y_max)
    
    
    for i in enemy_list:
        draw_enemy(i)
    
        



    
    # Swap buffers for smooth rendering (double buffering)
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
