import copy
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random, math


fovY = 120  # How wide the camera can see in vertical direction
grid_length = 50  # Length of grid lines


#game stat
stat = "restarted"
score = 0
bullets = 10
life = 5
cheat = False
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

    "theta" : math.radians(-90),  # for movement direction
    "rot_theta" : 0, # angle of rotation about z-axis
}

temp = copy.deepcopy(man)

# bullet
bullet = []

# enemy object
enemy = {
    "head" : {"create": [10, 10, 10], 
              "color": (0.251, 0.251, 0.251), 
              "position": [50, 320, 50]},


    "body" : {"create": [25, 100, 100], 
              "color": (1, 0, 0), 
              "position": [50, 320, 50-10-12]},
}

enemy_list = []


#camera position
camera_pos = [50, -50, 80]
camera_center = [50, 0,  80]
cam_temp_pos = camera_pos.copy()
camera_temp_center = camera_center.copy() 
third_person_view = True  
cam_angle = math.radians(-90)

#movement
step_size = 5
h_max = 50
h_min = 0
x_max = 375
x_min = -275
y_max = 640
y_min = -9


def updateCameraPosition():
    global camera_pos, camera_center, cam_angle

    
    dx = camera_pos[0] - camera_center[0]
    dy = camera_pos[1] - camera_center[1]
    rad = math.sqrt(dx**2 + dy**2)

    
    camera_pos[0] = camera_center[0] + rad * math.cos(cam_angle)
    camera_pos[1] = camera_center[1] + rad * math.sin(cam_angle)




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
    gluPerspective(fovY, 1.47, 0.1, 1500) 

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

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 680)  # left, right, bottom, top

    
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



def restart():
    global man, bullet, enemy_list, score, bullets, life, temp, camera_center, camera_pos, x_min, x_max, y_min, y_max
    bullets = 10
    life = 5
    score = 0
    enemy_list.clear()
    bullet.clear()
    man = copy.deepcopy(temp)
    camera_pos = [50, -20, 180] 
    camera_center = [50, 120, 20]
    enemy_creation(x_min, x_max, y_min, y_max)



def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """

    global man, step_size,  x_max , x_min , y_max , y_min, cheat
    
    
    # Move forward (W key)
    if key == b'w':
       x = step_size * math.cos(man["theta"])
       y = step_size * math.sin(man["theta"])
       new_x = man["head"]["position"][0] + x
       new_y = man["head"]["position"][1] + y

       if new_x < x_min + 10 or new_x > x_max - 10 and new_y < y_min + 10 or new_y > y_max - 10:
           x = 0
           y = 0

       man["head"]["position"][0] += x 
       man["head"]["position"][1] += y

       
       man["body"]["position"][0] += x
       man["body"]["position"][1] += y

       for a in man["arms"]:
           a["position"][0] += x 
           a["position"][1] += y

       for l in man["legs"]:
           l["position"][0] += x
           l["position"][1] += y

       man["gun"]["position"][0] += x
       man["gun"]["position"][1] += y



    # Move backward (S key)
    if key == b's':
       x = step_size * math.cos(man["theta"])
       y = step_size * math.sin(man["theta"])
       new_x = man["head"]["position"][0] - x
       new_y = man["head"]["position"][1] - y

       if new_x < x_min + 10 or new_x > x_max - 10 and new_y < y_min + 10 or new_y > y_max - 10:
           x = 0
           y = 0

       man["head"]["position"][0] -= x  
       man["head"]["position"][1] -= y

       man["body"]["position"][0] -= x
       man["body"]["position"][1] -= y

       for a in man["arms"]:
           a["position"][0] -= x
           a["position"][1] -= y

       for l in man["legs"]:
           l["position"][0] -= x
           l["position"][1] -= y

       man["gun"]["position"][0] -= x
       man["gun"]["position"][1] -= y


    # Rotate gun left (A key)
    if key == b'a':
        man["rot_theta"] -= step_size 
        man["rot_theta"] %= 360
        man["theta"] = math.radians(man["rot_theta"] - 90)
        
  
        

    # Rotate gun right (D key)
    if key == b'd':
        man["rot_theta"] += step_size  
        man["rot_theta"] %= 360
        man["theta"] = math.radians(man["rot_theta"] - 90)

    # # Toggle cheat mode (C key)
    if key == b'c':
        cheat = not cheat
        

    # # Toggle cheat vision (V key)
    # if key == b'v':

    # Reset the game if R key is pressed
    if key == b'r':
        restart()
    

def specialKeyListener(key, x, y):

    global camera_pos, step_size, camera_center, cam_angle
    

   
    dx = camera_center[0] - camera_pos[0]
    dy = camera_center[1] - camera_pos[1]
    dz = camera_center[2] - camera_pos[2]

    # Normalize the direction vector
    mod = math.sqrt(dx * dx + dy * dy + dz * dz)
    if mod != 0:
        dx /= mod
        dy /= mod
        dz /= mod

    
    if key == GLUT_KEY_UP: 
        camera_pos[0] += dx * step_size
        camera_pos[1] += dy * step_size
        camera_pos[2] += dz * step_size


        camera_center[0]  += dx * step_size
        camera_center[1]  += dy * step_size
        camera_center[2]  += dz * step_size


        

    elif key == GLUT_KEY_DOWN:  
        
        camera_pos[0] -= dx * step_size
        camera_pos[1] -= dy * step_size
        camera_pos[2] -= dz * step_size


        camera_center[0]  -= dx * step_size
        camera_center[1]  -= dy * step_size
        camera_center[2]  -= dz * step_size

    elif key == GLUT_KEY_RIGHT:
        if cam_angle < -math.pi/4:
            cam_angle += math.pi/16
            updateCameraPosition()

    elif key == GLUT_KEY_LEFT:
        if cam_angle > -3* math.pi/4:
            cam_angle -= math.pi/16
            updateCameraPosition()

    glutPostRedisplay()
        
      
    

def draw_bullet(pos):
    global bullet
    glPushMatrix()
    r, g, b = (0.36,0.25,0.20)        
    glTranslatef(pos[0], pos[1], pos[2])
    glColor3f(r,g,b)
    glutSolidCube(10) 
    glPopMatrix()

def mouseListener(button, state, x, y):
    
    global camera_pos, camera_center, third_person_view

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # print("Player fired bullets!")
        pos = []
        for i in range(3):
            pos.append(man["gun"]["position"][i])

        pos[0] += man["gun"]["height"] * math.cos(man["theta"])
        pos[1] += man["gun"]["height"] * math.sin(man["theta"])
        bullet.append([pos[0], pos[1], pos[2], man["theta"]]) 
        draw_bullet([pos[0], pos[1], pos[2]])

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:

        third_person_view = not third_person_view 
        if third_person_view:
            camera_pos = cam_temp_pos.copy()
            camera_center = camera_temp_center.copy()
        glutPostRedisplay()
    



    


def idle():
    global enemy_list, man, x_max, x_min, y_max, y_min, bullet, bullets, score
    if bullets == 0:
        game_over(man)
    # enemy movement
    
    step_size = 0.1
    hx = man['head']['position'][0]
    hy = man['head']['position'][1]
    for i in enemy_list:
        x = i["head"]["position"][0]
        y = i["head"]["position"][1]

        if hx > x:
            i["head"]["position"][0] += random.uniform(0, step_size)
            i["body"]["position"][0] += random.uniform(0, step_size)
        elif hx < x:
            i["head"]["position"][0] -= random.uniform(0, step_size)
            i["body"]["position"][0] -= random.uniform(0, step_size)
        
        if hy > y:
            i["head"]["position"][1] += random.uniform(0, step_size)
            i["body"]["position"][1] += random.uniform(0, step_size)
        elif hy < y:
            i["head"]["position"][1] -= random.uniform(0, step_size)
            i["body"]["position"][1] -= random.uniform(0, step_size)

    # bullet movement
    new_bullets = []
    for b in bullet:
        angle = b[3]
        x_move = step_size * math.cos(angle)
        y_move = step_size * math.sin(angle)

        new_x = b[0] - x_move
        new_y = b[1] - y_move

        
        if (new_x < x_min + 10 or new_x > x_max - 10) or (new_y < y_min + 10 or new_y > y_max - 10):
            bullets -= 1
            
                
            continue  

        hit_enemy = False
        for enemy in enemy_list[:]:  
            xe = enemy["body"]["position"][0]
            ye = enemy["body"]["position"][1]
            if xe - 12 <= new_x <= xe + 12 and ye - 12 <= new_y <= ye + 12:
                enemy_list.remove(enemy)
                score += 1
                enemy_creation1(x_min, x_max, y_min, y_max)
                hit_enemy = True
                break
 

        if not hit_enemy:
            new_bullets.append([b[0] + x_move * 5, b[1] + y_move * 5, b[2], angle])

    bullet = new_bullets

    #3rd person view
    global third_person_view, camera_pos, camera_center

    if not third_person_view:
        hx, hy, hz = man["head"]["position"]
        theta = man["theta"]

        cam_distance = 20  
        cam_height = 10    

        dx = -math.cos(theta)
        dy = -math.sin(theta)

        camera_pos = [
            hx + dx * cam_distance,
            hy + dy * cam_distance,
            hz + cam_height
        ]

        forward_distance = 50  
        camera_center = [
            hx + math.cos(theta) * forward_distance,
            hy + math.sin(theta) * forward_distance,
            hz
        ]

    
    if cheat:
             man["rot_theta"] += 5 
             man["rot_theta"] %= 360
             man["theta"] = math.radians(man["rot_theta"] - 90)

    #man dead
    check_collision(man["body"]["position"], enemy_list)
    if life == 0:
        game_over(man)
    # print("Player Remaining life: ", life)
    # print("Player Missed Bullets: ", 10 - bullets)


    #text
    draw_text(10, 670, f"Player Life Remaining {life}")
    draw_text(10, 640, f"Bullets Missed: {10 - bullets}")
    draw_text(10, 500, f"Current Score: {score}")
    glutPostRedisplay()

def game_over(man):
    
    glPushMatrix()
    body_pos = man["body"]["position"]
    center = body_pos[2] - (man["body"]["create"][2] / 2)  # base center of the cube
    
    glTranslatef(body_pos[0], body_pos[1], center)
    glRotatef(90, 0, 1, 0)
    glTranslatef(-body_pos[0], -body_pos[1], -center)

    draw_man()
    glPopMatrix()

    bullet.clear()
    enemy_list.clear()
    
    

    

def distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 +
                     (pos1[1] - pos2[1]) ** 2 +
                     (pos1[2] - pos2[2]) ** 2)



def enemy_creation1(x_min, x_max, y_min, y_max):
    global enemy, enemy_list, stat, man
    
    
    
    r = enemy["body"]["create"][0]

    x = random.uniform(x_min + r, x_max - r)
    y = random.uniform(y_min + r, y_max - r)
    if man["head"]["position"][0] == x and man["head"]["position"][1] == y:
        x = random.uniform(x_min + r, x_max - r)
        y = random.uniform(y_min + r, y_max - r)
        

    enemy["body"]["position"][0] = x
    enemy["body"]["position"][1] = y

    enemy["head"]["position"][0] = x
    enemy["head"]["position"][1] = y
    enemy_list.append(copy.deepcopy(enemy))

def check_collision(man, enemies, threshold=20):
    global life
    pos = man

    for enemy in enemies:
        enemy_pos = enemy["body"]["position"]
        dist = distance(pos, enemy_pos)

        if dist < threshold:
            life -= 1  # decrease health by 1
        if life < 0:
            game_over(man)            

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
    global enemy, enemy_list, stat, man
    
    
    for i in range(5):
        r = enemy["body"]["create"][0]

        x = random.uniform(x_min + r, x_max - r)
        y = random.uniform(y_min + r, y_max - r)
        if man["head"]["position"][0] == x and man["head"]["position"][1] == y:
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
    global grid_length, enemy_list, stat , h_max , h_min , x_max , x_min , y_max , y_min 
  
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 680)

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
    
    boundary = [
                 [[x_min,y_min, h_min],[x_min,y_min, h_max],[x_max, y_min, h_max],[x_max, y_min, h_min]], 
                 [[x_min,y_min, h_min],[x_min,y_min, h_max],[x_min, y_max, h_max],[x_min, y_max, h_min]], 
                 [[x_max,y_min, h_min],[x_max,y_min, h_max],[x_max, y_max, h_max],[x_max, y_max, h_min]], 
                 [[x_min,y_max, h_min],[x_min,y_max, h_max],[x_max, y_max, h_max],[x_max, y_max, h_min]]
               ]
    for i in range(len(boundary)):
        draw_boundary(i, boundary[i])
    
    
    #man
    draw_man()


    #enemy
    if stat == "restarted":
        enemy_creation(x_min, x_max, y_min, y_max)
    
    
    for i in enemy_list:
        draw_enemy(i)
    
        

    #bullet
    for pos in range(len(bullet)):
        draw_bullet(bullet[pos])

    
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
