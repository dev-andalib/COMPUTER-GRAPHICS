from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math, random
from heapq import heappush, heappop


######################################### Print on Screen ################################################
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



def draw_trea_status():
    y_offset = 0

    for tid in sorted(trea_names.keys()):
        name = trea_names[tid]
        count = trea_counts.get(tid, 0)  # Default to 0 if not yet collected
        text = f"{name}: {count}"

        # Set color: yellow if count > 0, else white
        if count > 0:
            glColor3f(1.0, 1.0, 0.0)  # Bright yellow
        else:
            glColor3f(1.0, 1.0, 1.0)  # White

        draw_text(740, 680 - y_offset, text)
        y_offset += 25

######################################### Print on Screen ################################################





######################################## Buttons ##############################################
buttons = [
    {"id": "pause",   "x": 440, "y": 650, "w": 30, "h": 30},
    {"id": "restart", "x": 490, "y": 650, "w": 30, "h": 30},
    {"id": "exit",    "x": 540, "y": 650, "w": 30, "h": 30},
]



paused = False

def restart_game():
    global man, life, trea_col, trea_use, trea_counts, game_r, paused, buttons
    
    game_r = True
    buttons[0][id] = 'play'
    paused = False
    life = 5
    trea_col.clear()
    trea_use.clear()
    for k in trea_counts.keys():
        trea_counts[k] = 0
    
    ########################################### MAN ######################################
    man['head']['position'] = [50, 400, 80]
    man['body']['position'] = [50, 400, 80-20-25]
    for i in range(len(man["legs"])):
        if i == 0:
            man["legs"][i]["position"] = [50 + 8, 400, 45 - 15 - 10]
        else:
            man["legs"][i]["position"] = [50 - 8, 400, 45 - 15 - 10]
    
    for i in range(len(man["arms"])):
        if i == 0:
            man["arms"][i]["position"] = [50 + 20, 400, 45 ]
        else:
            man["arms"][i]["position"] = [50 - 20, 400, 45 ]

    man["theta"] =  math.radians(-90)
    man["rot_theta"] = 0
    man["halo"] = None
    
    main()

def draw_buttons():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)  # Match your window size

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    
    for btn in buttons:
        x, y, w, h = btn["x"], btn["y"], btn["w"], btn["h"]
        cx = x + w / 2
        cy = y + h / 2

        # Draw rounded background (simple rectangle for now)
        glColor3f(0.2, 0.2, 0.2)  # Dark background
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + w, y)
        glVertex2f(x + w, y + h)
        glVertex2f(x, y + h)
        glEnd()

        # Border
        glColor3f(0.9, 0.9, 0.9)
        glLineWidth(2)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x, y)
        glVertex2f(x + w, y)
        glVertex2f(x + w, y + h)
        glVertex2f(x, y + h)
        glEnd()

        
        # Draw icon
        if btn["id"] == "play":
            glColor3f(0.0, 1.0, 0.5)
            glPushMatrix()
            glTranslatef(cx, cy, 0)
            glRotatef(180, 0, 0, 1)
            glBegin(GL_TRIANGLES)
            glVertex2f(-10, -10)
            glVertex2f(10, 0)
            glVertex2f(-10, 10)
            glEnd()
            glPopMatrix()
        
        if btn["id"] == "pause":
            glColor3f(0.0, 1.0, 0.5) 
            glPushMatrix()
            glTranslatef(cx, cy, 0)   
            glBegin(GL_QUADS)
                
            glVertex2f(-8, -10)
            glVertex2f(-4, -10)
            glVertex2f(-4, 10)
            glVertex2f(-8, 10)

           
            glVertex2f(4, -10)
            glVertex2f(8, -10)
            glVertex2f(8, 10)
            glVertex2f(4, 10)
            glEnd()

            glPopMatrix()

        elif btn["id"] == "restart":
            glColor3f(0.3, 0.8, 1.0)
            # Circular arrow
            glBegin(GL_LINE_STRIP)
            for angle in range(0, 270, 15):
                rad = math.radians(angle)
                glVertex2f(cx + 10 * math.cos(rad), cy + 10 * math.sin(rad))
            glEnd()

            glBegin(GL_TRIANGLES)
            glVertex2f(cx + 5, cy)
            glVertex2f(cx + 12, cy + 5)
            glVertex2f(cx + 12, cy - 5)
            glEnd()


        elif btn["id"] == "exit":
            glColor3f(1.0, 0.4, 0.4)
            glLineWidth(3)
            glBegin(GL_LINES)
            glVertex2f(x + 8, y + 8)
            glVertex2f(x + w - 8, y + h - 8)
            glVertex2f(x + w - 8, y + 8)
            glVertex2f(x + 8, y + h - 8)
            glEnd()

    # Restore previous matrix modes
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
######################################## Buttons ##############################################




##################################### Camera-related variables ##########################################
camera_pos = (0, 500, 500)
is_top = False

fovY = 120  # Field of view
GRID_LENGTH = 800  # Length of grid lines
rand_var = 423


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
    lx, ly, lz = (0, 0, 0)



    x = man["head"]["position"][0] + 50 * math.cos(man["theta"])
    y = man["head"]["position"][1] + 50 * math.sin(man["theta"])
    z = man["head"]["position"][2] + 20
    look_ahead = 100
    lx = x + look_ahead * math.cos(math.radians(man["rot_theta"] + math.radians(90)))
    ly = y + look_ahead * math.sin(math.radians(man["rot_theta"] + math.radians(90)))
    lz = z



    # Position the camera and set its orientation
    gluLookAt(x, y, z,  # Camera position
              lx, ly, lz,  # Look-at target
              0, 0, 1)  # Up vector (z-axis)
##################################### Camera-related variables ##########################################










##################################### Maze Wall ##########################################
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
            [-550, 70, -550, 320],
            [-800, -250, -250, -250],
            [-550, -800, -550, -500]]
x_min = maze_wall[0][0]
x_max = maze_wall[0][2]
y_min = maze_wall[1][1]
y_max = maze_wall[1][2]

def draw_maze():
    glPushMatrix()
    glColor3f(0, 0, 1)  # Maze wall color (white)

    
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


def wall_check(crr_pos, next_pos):
    global maze_wall

    x1 = crr_pos[0]
    y1 = crr_pos[1]

    x2 = next_pos[0]
    y2 = next_pos[1]

    temp = maze_wall

    
    
    
    for i in temp:
        global pass_through
        wx1, wy1, wx2, wy2 = i
        
        if wx1 == wx2:
                
                if min(x1, x2) <= wx1 <= max(x1, x2):
                    
                    if max(min(y1, y2), min(wy1, wy2)) <= min(max(y1, y2), max(wy1, wy2)):
                        
                        if pass_through and temp.index(i) not in [0,1,2,3]:
                            pass_through = False
                            return "norm"
                        return "hit"

       
        elif wy1 == wy2:
                if min(y1, y2) <= wy1 <= max(y1, y2):
                
                    if max(min(x1, x2), min(wx1, wx2)) <= min(max(x1, x2), max(wx1, wx2)):
                        if pass_through and temp.index(i) not in [0,1,2,3]:
                            pass_through = False
                            return "norm"
                        return "hit"
        
        else: 
                return "norm"
##################################### Maze Wall ##########################################




############################################### Game stat ############################################
game_r = True
top_view = 3
life = 5
############################################### Game stat ############################################





######################################## Teleport ######################################################
tele_cor = [(590, 710), (440, 180), (-355, 430), (320, 650), (660, 90), (90, 380), (100, 720), (-390, 320)]
tele_dis = 100 
tele_update = True
tele_i1 = None 
tele_i2 = None
target_tele = None


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
    global tele_i1, tele_i2, tele_update, tele_dis, target_tele 
    
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
            target_tele = 1
    else:
            tele_dis = temp1
            target_tele = 2
######################################## Teleport ######################################################



######################################### TREASSURES ###################################################
trea_names = {
    1: "ELIXIR OF IMMORTALITY",
    2: "EYE OF AVARICE",
    3: "HALO OF INVINCIBILITY",
    4: "RING OF PERMEATION"
}

trea_counts = {
    1: 0,
    2: 0,
    3: 0,
    4: 0
}



class Elixir:
    def __init__(self, pos):
        self.pos = pos
        self.r = 20
        self.h = 40
        self.id = 1
        self.dis = 0
        self.rand = random.randint(5, 255)


    def draw(self):
        glPushMatrix()
        glColor3f(0.4, 0.0, 0.0)
        glTranslatef(self.pos[0], self.pos[1], self.pos[2]-self.r/4)
        glutSolidSphere(self.r, 60, 60)
        glPopMatrix()

        glPushMatrix()       
        glTranslatef(self.pos[0], self.pos[1], self.pos[2])
        glColor3f(0.4, 0.0, 0.0)
        glutSolidCone(self.r, self.h, 60, 60)
        glPopMatrix()
    

    def function_on(self):
        
        global life, immortal
        life = 10
        immortal = True
        

         


    def function_off(self):
        global immortal
        immortal = False
        
   
   
class Avarice:
    def __init__(self, pos):
        self.Beye = 20
        self.Seye = 10
        self.pos = pos
        self.id = 2
        self.dis = 0
        self.rand = random.randint(5, 255)

        #power related var
        self.cam = None
        self.top = (0, 50, 800)
        self.count = 0
       

    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], self.pos[2])
        glColor3f(1.0, 1.0, 1.0)  # White
        glScalef(1.5, 1.0, 1.0)  # Stretch horizontally (X-axis)
        glutSolidSphere(self.Beye, 50, 50)
        glPopMatrix()

        # iris,red, stretched(glscalef)
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], self.pos[2])
        glColor3f(1.0, 0.0, 0.0)
        glutSolidSphere(self.Seye, 50, 50)
        glPopMatrix()

    
    def function_on(self, pos):
        global is_top, top_view
        if not is_top and top_view > 0:
            is_top = True
            self.cam = pos
        top_view -= 1
        return self.top



    def function_off(self):
        global is_top

        is_top = False
        return self.cam
        
            

class Halo:
    def __init__(self, pos):
        self.inner_r = 5
        self.outer_r = 30
        self.pos = pos
        self.id = 3
        self.dis = 0
        self.rand = random.randint(5, 255)


        
       

    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], self.pos[2])
        glColor3f(1.0, 0.84, 0.0)  # Golden color
        
        glutSolidTorus(self.inner_r, self.outer_r, 30, 60)
        glPopMatrix()


    def function_on(self, man):
        pos = man["head"]["position"]
        man["halo"] = Halo([pos[0], pos[1], pos[2]+30])
        

    def function_off(self, man):
        man["halo"] = None
        
        

class Perme:
    def __init__(self, pos):
        self.inner_r = 5
        self.outer_r = 30
        self.pos = pos
        self.id = 4
        self.dis = 0
        self.rand = random.randint(5, 255)
        
        

    def draw(self):
        # Draw the thinner, golden ring
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], self.pos[2])
        glColor3f(0.8, 0.85, 0.9)
        glutSolidTorus(self.inner_r, self.outer_r, 30, 60)
        glPopMatrix()

        #Draw the diamond
        glPushMatrix()
        glTranslatef(self.pos[0]-self.inner_r * 8, self.pos[1], self.pos[2])
        glRotatef(45, 1, 0, 0)
        glScalef(15,15,15)
        glColor3f(0.95, 0.95, 1.0)
        glutSolidOctahedron()
        glPopMatrix()

    def function_on(self):
        global pass_through
        pass_through = True
        

is_top = False
immortal = False
pass_through = False


trea_col = []
trea_cor = [(552, 370), (362,374), (378, 230), (-106, 380), 
            (324, 533), (-559, -121), (273, -241), (86, -250)]

treai = None
sel_t1 = None
sel_t2 = None

trea_use = []


def treasure_manage():
    global treai, sel_t1, sel_t2, trea_col

    sel_t1 = random.randint(0,len(trea_cor)-1)
    sel_t2 = random.randint(0,len(trea_cor)-1)
    if sel_t1 == sel_t2:
        sel_t2 = random.randint(0,len(trea_cor)-1)
    
    coor = [
            [trea_cor[sel_t1][0], trea_cor[sel_t1][1], 60], 
            [trea_cor[sel_t2][0], trea_cor[sel_t2][1], 60]
           ]
    
    for i in range(2):
        treai = random.randint(1,4)
        if treai == 1:
            obj = Elixir(coor[i])
            trea_col.append(obj)
        
        elif treai == 2:
            obj = Avarice(coor[i])
            trea_col.append(obj)
        

        elif treai == 3:
            obj = Halo(coor[i])
            trea_col.append(obj)
        

        elif treai == 4:
            obj = Perme(coor[i])
            trea_col.append(obj)
        

def draw_trea():
    global trea_col

    for i in trea_col:
        i.draw()

def remove_trea(i, col):
    col.pop(col.index(i))
    


def get_trea():
    global trea_col, trea_use 
    for i in trea_col: 
        pos = i.pos
        temp = math.pow(math.pow(man["head"]["position"][0] - pos[0], 2) + math.pow(man["head"]["position"][1] - pos[1], 2) , 0.5)
        i.dis = temp

        if i.dis < 50:
            trea_use.append(i)
            if i.id == 1:
                trea_counts[i.id] += 1

            elif i.id == 2:
                trea_counts[i.id] += 1
            

            elif i.id == 3:
                trea_counts[i.id] += 1

            
            elif i.id == 4:
                trea_counts[i.id] += 1



            remove_trea(i, trea_col)
             

def activate_power(tid):
    global trea_use, camera_pos, man

    for obj in trea_use:
        if obj.id == tid:
            i = obj
            break
    
    
    if i.id == 1 and  trea_counts[i.id]>0:
        i.function_on()
        if i.id == 1:
            trea_counts[i.id] -= 1
        
    elif i.id == 2 and  trea_counts[i.id]>0:
        camera_pos = i.function_on(camera_pos)
        if i.id == 2:
            trea_counts[i.id] -= 1
        
    elif i.id == 3 and  trea_counts[i.id]>0:
        i.function_on(man)
        if i.id == 3:
            trea_counts[i.id] -= 1
        
    elif i.id == 4 and  trea_counts[i.id]>0:
        i.function_on()
        if i.id == 4:
            trea_counts[i.id] -= 1
            remove_trea(i, trea_use)
    
    

def deactivate_power(tid):
    global trea_use, camera_pos, man
    
    for i in trea_use:
        i.id = tid
        break

    
    if i.id == 1:
        i.function_off()

    elif i.id == 2:
        camera_pos = i.function_off()
        
    elif i.id == 3:
        i.function_off(man)
    remove_trea(i, trea_use)


    
####################### TREASSURES ###################################################


################################ MAN #########################################################
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


    

    "theta" : math.radians(-90),  # for movement direction
    "rot_theta" : 0, # angle of rotation about z-axis
    "type" : "player",
    "halo" : None,
} 
step_size = 5
def draw_man():
    global man, immortal, rain
    
    
        
    #rotate as a whole
    glPushMatrix()


    body_pos = man["body"]["position"]
    center = body_pos[2] - (man["body"]["create"][2] / 2)  # base center of the cube
    
    glTranslatef(body_pos[0], body_pos[1], center)
    glRotatef(man["rot_theta"], 0, 0, 1)
    glTranslatef(-body_pos[0], -body_pos[1], -center)
    #arms 


    if immortal:
        glPushMatrix()
        c = random.randint(0,1)
        if c == 0:   glColor3f(144/255, 238/255, 144/255)
        else:  glColor3f(0.133, 0.545, 0.133)
        pos = man["head"]["position"]
        glTranslatef(pos[0], pos[1], 2) 
        gluCylinder(gluNewQuadric(),  50, 40, 0, 100, 100 ) 
        gluCylinder(gluNewQuadric(),  30, 20, 0, 100, 100 )         
        glPopMatrix()

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

    if man["halo"] != None:
        obj = man["halo"]
        pos = man["head"]["position"]
        obj.pos = [ pos[0], pos[1], pos[2]+30 ]        
        obj.draw()

    glPopMatrix()
def spawn(obj, x, y):
    global tele_i2, tele_i1, tele_cor,  target_tele
    
    

    if obj["type"] == "player":    
        man["head"]["position"][0] = x 
        man["head"]["position"][1] = y

       
        man["body"]["position"][0] = x
        man["body"]["position"][1] = y

        i = 0
        for a in man["arms"]:
           if i == 0: a["position"][0] = x + 20
           else:      a["position"][0] = x - 20
           
           a["position"][1] = y
           i += 1


        i = 0
        for l in man["legs"]:
           if i == 0: l["position"][0] = x + 8
           else:      l["position"][0] = x - 8

           l["position"][1] = y
           i += 1
################################ MAN #########################################################



############################## ENEMY #####################################################
frame_count = 0
enemy_positions = []
enemy_paths = []  # Store paths for each enemy
enemy_speeds = [0.3 for _ in range(3)]  # Increased speed for noticeable movement


def is_valid_position(x, y, buffer=30):
    for wall in maze_wall:
        x1, y1, x2, y2 = wall
        if min(x1, x2) - buffer <= x <= max(x1, x2) + buffer and min(y1, y2) - buffer <= y <= max(y1, y2) + buffer:
            return False
    return True


def spawn_enemies(n=3):
    global enemy_paths
    attempts = 0
    enemy_positions.clear()
    enemy_paths = [[] for _ in range(n)]
    while len(enemy_positions) < n and attempts < 1000:
        x = random.randint(-700, 700)
        y = random.randint(-700, 700)
        if is_valid_position(x, y, buffer=100):  # Larger buffer for spawning
            enemy_positions.append([x, y])
        attempts += 1


def heuristic(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def get_neighbors(pos, grid_size=30):
    x, y = pos
    neighbors = [
        (x + grid_size, y), (x - grid_size, y),
        (x, y + grid_size), (x, y - grid_size)
    ]
    return [(nx, ny) for nx, ny in neighbors if -800 <= nx <= 800 and -800 <= ny <= 800 and is_valid_position(nx, ny)]


def a_star(start, goal, grid_size=30):
    start = (round(start[0] / grid_size) * grid_size, round(start[1] / grid_size) * grid_size)
    goal = (round(goal[0] / grid_size) * grid_size, round(goal[1] / grid_size) * grid_size)

    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current_f, current = heappop(open_set)

        if heuristic(current, goal) < grid_size:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for neighbor in get_neighbors(current, grid_size):
            tentative_g = g_score[current] + heuristic(current, neighbor)

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                heappush(open_set, (f_score[neighbor], neighbor))

    return []


def update_enemy_paths():
    global frame_count
    if frame_count % 10 == 0:  
        player_pos = man["body"]["position"][:2]
        for i, enemy_pos in enumerate(enemy_positions):
            path = a_star((enemy_pos[0], enemy_pos[1]), player_pos)
            enemy_paths[i] = path
    frame_count += 1


def move_enemy(enemy_idx):
    if not enemy_paths[enemy_idx]:
        return

    enemy_pos = enemy_positions[enemy_idx]
    target = enemy_paths[enemy_idx][0]

    dx = target[0] - enemy_pos[0]
    dy = target[1] - enemy_pos[1]
    dist = math.sqrt(dx ** 2 + dy ** 2)

    if dist < enemy_speeds[enemy_idx]:
        enemy_pos[0], enemy_pos[1] = target
        enemy_paths[enemy_idx].pop(0)
    else:
        move_dist = enemy_speeds[enemy_idx] / dist
        enemy_pos[0] += dx * move_dist
        enemy_pos[1] += dy * move_dist

def draw_enemy(x, y):
    glPushMatrix()
    glTranslatef(x, y, 30)
    glColor3f(1, 0, 0)
    gluSphere(gluNewQuadric(), 30, 20, 20)
    glPushMatrix()
    glColor3f(0.8, 0.8, 0.1)
    glTranslatef(-15, 0, 30)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 1, 30, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glColor3f(0.8, 0.8, 0.1)
    glTranslatef(15, 0, 30)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 1, 30, 10, 10)
    glPopMatrix()
    glPopMatrix()
############################## ENEMY #####################################################


def keyboardListener(key, x, y):

    global step_size, is_top, paused

       
     # Move forward (W key)
    if key == b'w' and not paused  and not is_top:
       curr_x, curr_y = man["head"]["position"][0], man["head"]["position"][1]
       x = step_size * math.cos(man["theta"])
       y = step_size * math.sin(man["theta"])
       new_x = man["head"]["position"][0] + x
       new_y = man["head"]["position"][1] + y


       
       
       stat = wall_check((curr_x, curr_y), (new_x, new_y))
       if stat == 'hit' or top_view == True:
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

       



    # Move backward (S key)
    if key == b's' and not paused  and not is_top:
       curr_x, curr_y = man["head"]["position"][0], man["head"]["position"][1]


       x = step_size * math.cos(man["theta"])
       y = step_size * math.sin(man["theta"])
       new_x = man["head"]["position"][0] - x
       new_y = man["head"]["position"][1] - y

       

       stat = wall_check((curr_x, curr_y), (new_x, new_y))
       if stat == 'hit' or is_top == True:
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

       


    # Rotate gun left (A key)
    if key == b'd' and not is_top and not paused:
        man["rot_theta"] -= step_size 
        man["rot_theta"] %= 360
        man["theta"] = math.radians(man["rot_theta"] - 90)
        
  
        

    # Rotate gun right (D key)
    if key == b'a' and not is_top and not paused:
        man["rot_theta"] += step_size  
        man["rot_theta"] %= 360
        man["theta"] = math.radians(man["rot_theta"] - 90)


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
    global paused, buttons, is_top
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 740 < x < 985 and 100 < y < 115 and trea_counts[1]>0:
           activate_power(1)
        
        elif 740 < x < 915 and 125 < y < 145 and trea_counts[2]>0:
           activate_power(2)
        

        elif 740 < x < 975 and 155 < y < 170 and trea_counts[3]>0:
           activate_power(3)

        elif 740 < x < 960 and 180 < y < 200 and trea_counts[4]>0:
           activate_power(4)
        

        elif 440 < x < 470 and 120 < y < 150:
            
            if paused == False:
                paused = True
                buttons[0]['id'] = 'play'
            
            elif paused == True:
                paused = False
                buttons[0]['id'] = 'pause'
            
            
        
        elif 490 < x < 520 and 120 < y < 150:
            restart_game()
        

        elif 540 < x < 565 and 120 < y < 150:
            game_exit = True
        

    # # Right mouse button toggles camera tracking mode
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN and is_top:
            deactivate_power(2)




def idle():
    global tele_update, tele_dis, tele_i1, tele_i2

    update_enemy_paths()
    for i in range(len(enemy_positions)):
        move_enemy(i)

    if tele_dis < 70:
        
        if target_tele == 1:
            x = tele_cor[tele_i1][0]
            y = tele_cor[tele_i1][1]
        else:
            x = tele_cor[tele_i2][0]
            y = tele_cor[tele_i2][1]
        tele_update = True
        teleport()
        spawn(man, x, y)

    

    get_trea()
    
    glutPostRedisplay()



def showScreen():
    global game_r, tele_update, trea_col, enemy_positions
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
    glColor3f(1.0, 1.0, 1.0)
    draw_text(10, 680, f"Top View Count: {top_view}")
    draw_text(10, 650, f"Lives: {life}")


    
    

    if game_r:
        game_r = False
        tele_update = True
        
    
    teleport()
    
    if len(trea_col) == 0:
        treasure_manage()

    draw_man()
    
    draw_trea()

    for pos in enemy_positions:
        draw_enemy(pos[0], pos[1])

    draw_maze()


    draw_buttons()

    draw_trea_status()

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
    spawn_enemies()
    glutMainLoop()  # Enter the GLUT main loop


if __name__ == "__main__":
    main()
