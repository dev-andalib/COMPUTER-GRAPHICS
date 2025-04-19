from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Camera-related variables
camera_pos = (0,500,500)

fovY = 120  # Field of view
length = 50  # Length of grid lines
rand_var = 423


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
    # if key == GLUT_KEY_UP:

    # # Move camera down (DOWN arrow key)
    # if key == GLUT_KEY_DOWN:

    # moving camera left (LEFT arrow key)
    if key == GLUT_KEY_LEFT:
        x -= 1  # Small angle decrement for smooth movement

    # moving camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        x += 1  # Small angle increment for smooth movement

    camera_pos = (x, y, z)


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
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, 1.25, 0.1, 1500) # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix

    # Extract camera position and look-at target
    x, y, z = camera_pos
    # Position the camera and set its orientation
    gluLookAt(x, y, z,  # Camera position
              0, 0, 0,  # Look-at target
              0, 0, 1)  # Up vector (z-axis)


def idle():
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    # Ensure the screen updates with the latest changes
    glutPostRedisplay()


def showScreen():
    global length
    grid_length = length
  
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)

    setupCamera()  # Configure camera perspective

   

    # Draw the grid (game floor)
    
    
    
    
    
    start = [-265,40]
    temp = start.copy()
    for i in range(13):
        for j in range(13):
            if j%2 == 0 and i%2 == 0:
                glBegin(GL_QUADS)
                glColor3f(1, 1, 1)
                glVertex3f(start[0], start[1], 0)
                glVertex3f(start[0]+grid_length, start[1], 0)
                glVertex3f(start[0]+grid_length, start[1]+grid_length, 0)
                glVertex3f(start[0], start[1]+grid_length, 0)
                glEnd()
                start[0] += 50
            

            elif j%2 != 0 and i%2 == 0:
                glBegin(GL_QUADS)
                glColor3f(0.7, 0.5, 0.95)
                glVertex3f(start[0], start[1], 0)
                glVertex3f(start[0]+grid_length, start[1], 0)
                glVertex3f(start[0]+grid_length, start[1]+grid_length, 0)
                glVertex3f(start[0], start[1]+grid_length, 0)
                glEnd()
                start[0] += 50
            

            elif j%2 == 0 and i%2 != 0:
                glBegin(GL_QUADS)
                glColor3f(0.7, 0.5, 0.95)
                glVertex3f(start[0], start[1], 0)
                glVertex3f(start[0]+grid_length, start[1], 0)
                glVertex3f(start[0]+grid_length, start[1]+grid_length, 0)
                glVertex3f(start[0], start[1]+grid_length, 0)
                glEnd()
                start[0] += 50
            

            elif j%2 != 0 and i%2 != 0:
                glBegin(GL_QUADS)
                glColor3f(1,1,1)
                glVertex3f(start[0], start[1], 0)
                glVertex3f(start[0]+grid_length, start[1], 0)
                glVertex3f(start[0]+grid_length, start[1]+grid_length, 0)
                glVertex3f(start[0], start[1]+grid_length, 0)
                glEnd()
                start[0] += 50
        start[1] += grid_length
        start[0] = temp[0]     
   
    boundary = [
                 [[-275,-10, 0],[-275,-10, height],[375, -10, height],[375, -10, 0]], 
                 [[-275,-10, 0],[-275,-10, height],[-275, 640, height],[-275, 640, 0]], 
                 [[375,-10, 0],[375,-10, height],[375, 640, height],[375, 640, 0]], 
                 [[-275,640, 0],[-275,640, height],[375, 640, height],[375, 640, 0]]
               ]
    
    for i in boundary:
        glBegin(GL_QUADS)
        glColor3f(0.75,0.75,0.75)
        for j in i:
            x = j[0] 
            y = j[1]
            z = j[2]
            glVertex3f(x, y, z)
        glEnd()

    # Display game info text at a fixed screen position
    

    
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
