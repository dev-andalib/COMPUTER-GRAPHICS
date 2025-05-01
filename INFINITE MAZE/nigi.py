from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

# Constants
GRID_LENGTH = 600
BULLET_SPEED = 15  # Increased bullet speed for better gameplay
ENEMY_SPEED = 0.1  # Slightly increased enemy speed
PLAYER_SIZE = 30
HOSTAGE_SIZE = 20
ENEMY_SIZE = 25
OBSTACLE_SIZE = 30
NUM_ENEMIES = 5
NUM_OBSTACLES = 10
MAX_MISSED_BULLETS = 20  # Increased max missed bullets
LEVEL_SCORE_THRESHOLD = 1000  # Score needed to advance to next level

# Variables
player_pos = [0, 0, 0]
player_angle = 0
player_lives = 5
game_score = 0
bullets_missed = 0
game_over = False
current_level = 1
emergency_shields = 2
shield_active = False
hostage_pos = [GRID_LENGTH // 2, GRID_LENGTH // 2, 0]  # Hostage position
obstacle_damage = [1, 2, 3]  # Damage for each obstacle type
# Camera
camera_pos = [0, 500, 500]
camera_angle_x = 45
camera_angle_y = 0
first_person = False
cheat_mode = False
cheat_vision = False

# Game object classes
class Bullet:
    def __init__(self, x, y, z, angle):
        self.x = x
        self.y = y
        self.z = z
        self.angle = angle
        self.distance = 0
        self.active = True

class Enemy:
    def __init__(self):
        self.reset()
        self.size = 1.0
        self.size_dir = 0.01

    def reset(self):
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(GRID_LENGTH * 0.7, GRID_LENGTH * 0.9)
        self.x = dist * math.cos(angle)
        self.y = dist * math.sin(angle)
        self.z = 0
        self.speed = ENEMY_SPEED

class Obstacle:
    def __init__(self, x, y, shape_type):
        self.x = x
        self.y = y
        self.z = 0
        self.shape_type = shape_type  # 0: cube, 1: sphere, 2:cylinder
        self.damage = obstacle_damage[shape_type] # store damage value

# Global lists
bullets = []
enemies = []
obstacles = []


def init_game():
    global player_pos, player_angle, player_lives, game_score, bullets_missed, game_over, current_level, obstacles
    global bullets, enemies, camera_pos, camera_angle_x, camera_angle_y, emergency_shields, shield_active
    player_pos = [0, 0, 0]
    player_angle = 0
    player_lives = 5
    game_score = 0
    bullets_missed = 0
    game_over = False
    current_level = 1
    emergency_shields = 2
    shield_active = False
    bullets = []
    enemies = []
    obstacles = []  # Clear obstacles
    init_enemies()  # Initialize enemies based on level
    init_obstacles() # Initialize obstacles
    camera_pos = [0, 500, 500]
    camera_angle_x = 45
    camera_angle_y = 0

def init_enemies():
    """Initialize enemies based on the current level."""
    global enemies
    enemies = []
    if current_level == 1:
        for _ in range(NUM_ENEMIES):
            enemies.append(Enemy())
    elif current_level == 2:
        for _ in range(NUM_ENEMIES + 3):  # More enemies in level 2
            enemies.append(Enemy())
    elif current_level == 3:
        for _ in range(NUM_ENEMIES + 5):  # Even more enemies in level 3
            enemies.append(Enemy())

def init_obstacles():
    """Initialize obstacles with random positions and shapes."""
    global obstacles
    obstacles = []
    for _ in range(NUM_OBSTACLES):
        x = random.randint(-GRID_LENGTH // 2, GRID_LENGTH // 2)
        y = random.randint(-GRID_LENGTH // 2, GRID_LENGTH // 2)
        shape_type = random.randint(0, 2)  # 0: cube, 1: sphere, 2: cylinder
        obstacles.append(Obstacle(x, y, shape_type))

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_player():
    glPushMatrix()
    glTranslatef(*player_pos)
    glRotatef(player_angle, 0, 0, 1)

    # Main body
    glPushMatrix()
    glTranslatef(0, 0, 40)
    glScalef(30, 40, 60)
    glColor3f(0, 1, 0)
    glutSolidCube(1)
    glPopMatrix()

    # Head
    glPushMatrix()
    glTranslatef(0, 0, 80)
    glColor3f(0, 0, 0)
    glutSolidSphere(20, 20, 20)
    glPopMatrix()

    # Legs
    glPushMatrix()
    glTranslatef(10, -12, 0)
    glScalef(12, 15, 30)
    glColor3f(0, 0, 1)
    glutSolidCube(1)  # Left leg

    glTranslatef(0, 2, 0)
    glutSolidCube(1)  # Right leg
    glPopMatrix()

    # Shoulder joint
    glPushMatrix()
    glTranslatef(0, 0, 50)
    glColor3f(0.5, 0.5, 0.5)
    glutSolidSphere(10, 10, 10)

    # Arms
    glRotatef(90, 0, 1, 0)  # horizontal

    # Left arm
    glPushMatrix()
    glTranslatef(-10, -15, 25)
    gluCylinder(gluNewQuadric(), 6, 6, 50, 10, 10)
    glPopMatrix()

    # Right arm (extends forward right)
    glPushMatrix()
    glTranslatef(-10, 15, 25)
    gluCylinder(gluNewQuadric(), 6, 6, 50, 10, 10)
    glPopMatrix()

    # GUN
    glPushMatrix()
    glTranslatef(0, 0, 75)  # between arms
    glColor3f(0.5, 0.5, 0.5)

    # base
    glPushMatrix()
    glTranslatef(0, 0, 0)
    glScalef(25, 15, 15)  # connect both arms
    glutSolidCube(1)
    glPopMatrix()

    glPopMatrix()
    glPopMatrix()

    glPopMatrix()

def draw_hostage():
    glPushMatrix()
    glTranslatef(*hostage_pos)
    glScalef(HOSTAGE_SIZE, HOSTAGE_SIZE, HOSTAGE_SIZE)
    glColor3f(1, 1, 1)  # White
    glutSolidSphere(1, 20, 20)
    glPopMatrix()

def draw_enemies():
    for enemy in enemies:
        glPushMatrix()
        glTranslatef(enemy.x, enemy.y, enemy.z)
        glScalef(enemy.size, enemy.size, enemy.size)

        # Main body
        glPushMatrix()
        glTranslatef(0, 0, 15)
        glColor3f(1, 0, 0)  # Red
        glutSolidSphere(ENEMY_SIZE, 20, 20)
        glPopMatrix()
        # Head
        glPushMatrix()
        glTranslatef(0, 0, 45)
        glColor3f(0, 0, 0)
        glutSolidSphere(15, 20, 20)
        glPopMatrix()

        glPopMatrix()

def draw_bullets():
    for bullet in bullets:
        if bullet.active:
            glPushMatrix()
            glTranslatef(bullet.x, bullet.y, bullet.z)
            glColor3f(1, 1, 0)
            glutSolidCube(10)
            glPopMatrix()

def draw_obstacles():
    for obstacle in obstacles:
        glPushMatrix()
        glTranslatef(obstacle.x, obstacle.y, obstacle.z)
        glColor3f(0.4, 0.4, 0.4)  # Dark Gray
        if obstacle.shape_type == 0:  # Cube
            glutSolidCube(OBSTACLE_SIZE)
        elif obstacle.shape_type == 1:  # Sphere
            glutSolidSphere(OBSTACLE_SIZE // 2, 20, 20)
        elif obstacle.shape_type == 2:  # Cylinder
            gluCylinder(gluNewQuadric(), OBSTACLE_SIZE // 2, OBSTACLE_SIZE // 2, OBSTACLE_SIZE, 20, 20)
        glPopMatrix()

def draw_grid():
    grid_size = 70
    for x in range(-GRID_LENGTH, GRID_LENGTH, grid_size):
        for y in range(-GRID_LENGTH, GRID_LENGTH, grid_size):
            glBegin(GL_QUADS)
            if (x // grid_size + y // grid_size) % 2 == 0:
                glColor3f(0.9, 0.9, 0.9)
            else:
                glColor3f(0.1, 0.1, 0.1)
            glVertex3f(x, y, 0)
            glVertex3f(x + grid_size, y, 0)
            glVertex3f(x + grid_size, y + grid_size, 0)
            glVertex3f(x, y + grid_size, 0)
            glEnd()

    boundary_height = 50

    # North border
    glColor3f(1.0, 1.0, 0.0)  # Yellow
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, boundary_height)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, boundary_height)
    glEnd()

    # South border
    glColor3f(1.0, 0.0, 0.0)  # Red
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, boundary_height)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, boundary_height)
    glEnd()

    # East border
    glColor3f(0.0, 0.0, 1.0)  # Blue
    glBegin(GL_QUADS)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, boundary_height)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, boundary_height)
    glEnd()

    # West border
    glColor3f(0.0, 1.0, 0.0)  # Green
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, boundary_height)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, boundary_height)
    glEnd()

def update_bullets():
    global bullets_missed, game_score

    for bullet in bullets[:]:
        if not bullet.active:
            continue

        bullet.x += BULLET_SPEED * math.cos(math.radians(bullet.angle))
        bullet.y += BULLET_SPEED * math.sin(math.radians(bullet.angle))
        bullet.distance += BULLET_SPEED

        hit = False
        for enemy in enemies:
            dx = bullet.x - enemy.x
            dy = bullet.y - enemy.y
            distance = math.sqrt(dx * dx + dy * dy)
            if distance < ENEMY_SIZE:
                game_score += 10
                enemy.reset()
                hit = True
                bullet.active = False
                break

        if (abs(bullet.x) > GRID_LENGTH or abs(bullet.y) > GRID_LENGTH or
                bullet.distance > GRID_LENGTH * 2):
            bullet.active = False
            bullets_missed += 1

    bullets[:] = [b for b in bullets if b.active]

def update_enemies():
    global player_lives, game_over

    for enemy in enemies:
        dx = player_pos[0] - enemy.x
        dy = player_pos[1] - enemy.y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist > 0:
            enemy.x += enemy.speed * dx / dist
            enemy.y += enemy.speed * dy / dist

        if dist < PLAYER_SIZE and not shield_active:
            player_lives -= 1
            enemy.reset()

            if player_lives <= 0:
                game_over = True

        enemy.size += enemy.size_dir
        if enemy.size > 1.2 or enemy.size < 0.8:
            enemy.size_dir *= -1

def update_player_position():
    global player_pos
    player_pos[0] = max(-GRID_LENGTH + PLAYER_SIZE, min(GRID_LENGTH - PLAYER_SIZE, player_pos[0]))
    player_pos[1] = max(-GRID_LENGTH + PLAYER_SIZE, min(GRID_LENGTH - PLAYER_SIZE, player_pos[1]))

def check_obstacle_collision():
    global player_lives
    for obstacle in obstacles:
        dx = player_pos[0] - obstacle.x
        dy = player_pos[1] - obstacle.y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist < PLAYER_SIZE + OBSTACLE_SIZE // 2 and not shield_active:
            player_lives -= obstacle.damage
            if player_lives <= 0:
                global game_over
                game_over = True

def keyboardListener(key, x, y):
    global player_pos, player_angle, cheat_mode, cheat_vision, emergency_shields, shield_active

    if game_over and key == b'r':
        init_game()
        return

    if game_over:
        return

    key = key.decode('utf-8').lower()

    if key == 'w':
        player_pos[0] += 10 * math.cos(math.radians(player_angle))
        player_pos[1] += 10 * math.sin(math.radians(player_angle))
    elif key == 's':
        player_pos[0] -= 10 * math.cos(math.radians(player_angle))
        player_pos[1] -= 10 * math.sin(math.radians(player_angle))
    elif key == 'a' and not cheat_mode:
        player_angle = (player_angle + 10) % 360
    elif key == 'd' and not cheat_mode:
        player_angle = (player_angle - 10) % 360
    elif key == 'c':
        cheat_mode = not cheat_mode
    elif key == 'v' and cheat_mode:
        cheat_vision = not cheat_vision
    elif key == 'e' and emergency_shields > 0 and not shield_active:
        shield_active = True
        emergency_shields -= 1
        glutTimerFunc(3000, disable_shield, 0)  # Shield lasts 3 seconds

    update_player_position()

def disable_shield(value):
    global shield_active
    shield_active = False

def specialKeyListener(key, x, y):
    global camera_angle_x, camera_angle_y

    if key == GLUT_KEY_UP:
        camera_angle_x = min(90, camera_angle_x + 5)
    elif key == GLUT_KEY_DOWN:
        camera_angle_x = max(0, camera_angle_x - 5)
    elif key == GLUT_KEY_LEFT:
        camera_angle_y = (camera_angle_y + 5) % 360
    elif key == GLUT_KEY_RIGHT:
        camera_angle_y = (camera_angle_y - 5) % 360

def mouseListener(button, state, x, y):
    global bullets

    if game_over:
        return

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        bullet_x = player_pos[0] + 75 * math.cos(math.radians(player_angle))
        bullet_y = player_pos[1] + 75 * math.sin(math.radians(player_angle))
        bullet_z = player_pos[2] + 50  # Gun height
        bullets.append(Bullet(bullet_x, bullet_y, bullet_z, player_angle))
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        global first_person
        first_person = not first_person

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if first_person:
        if cheat_mode and cheat_vision:
            # Cheat vision mode - camera follows gun automatically
            eye_x = player_pos[0] + 20 * math.cos(math.radians(player_angle))
            eye_y = player_pos[1] + 20 * math.sin(math.radians(player_angle))
            eye_z = player_pos[2] + 80  # Head height

            # point slightly in front
            look_ahead = 100
            center_x = eye_x + look_ahead * math.cos(math.radians(player_angle))
            center_y = eye_y + look_ahead * math.sin(math.radians(player_angle))
            center_z = eye_z

            gluLookAt(eye_x, eye_y, eye_z,
                      center_x, center_y, center_z,
                      0, 0, 1)
        else:
            # Normal first-person view
            eye_x = player_pos[0] + 20 * math.cos(math.radians(player_angle))
            eye_y = player_pos[1] + 20 * math.sin(math.radians(player_angle))
            eye_z = player_pos[2] + 80  # Head height

            center_x = eye_x + math.cos(math.radians(player_angle))
            center_y = eye_y + math.sin(math.radians(player_angle))

            gluLookAt(eye_x, eye_y, eye_z,
                      center_x, center_y, eye_z,
                      0, 0, 1)
    else:
        # Third-person orbiting view
        dist = 500
        rad_x = math.radians(camera_angle_x)
        rad_y = math.radians(camera_angle_y)

        eye_x = player_pos[0] + dist * math.cos(rad_y) * math.cos(rad_x)
        eye_y = player_pos[1] + dist * math.sin(rad_y) * math.cos(rad_x)
        eye_z = player_pos[2] + dist * math.sin(rad_x)

        gluLookAt(eye_x, eye_y, eye_z,
                  player_pos[0], player_pos[1], player_pos[2],
                  0, 0, 1)

def cheat_mode_actions():
    global bullets, player_angle

    if not cheat_mode or game_over:
        return
    player_angle = (player_angle + 1) % 360

    if glutGet(GLUT_ELAPSED_TIME) % 100 == 0:
        bullet_x = player_pos[0] + 75 * math.cos(math.radians(player_angle))
        bullet_y = player_pos[1] + 75 * math.sin(math.radians(player_angle))
        bullet_z = player_pos[2] + 50
        bullets.append(Bullet(bullet_x, bullet_y, bullet_z, player_angle))

    if cheat_vision and first_person:
        # Find nearest enemy
        nearest_enemy = None
        min_dist = float('inf')
        for enemy in enemies:
            dx = enemy.x - player_pos[0]
            dy = enemy.y - player_pos[1]
            dist = math.sqrt(dx * dx + dy * dy)
            if dist < min_dist:
                min_dist = dist
                nearest_enemy = enemy

        # rotate toward nearest enemy
        if nearest_enemy:
            dx = nearest_enemy.x - player_pos[0]
            dy = nearest_enemy.y - player_pos[1]
            target_angle = math.degrees(math.atan2(dy, dx)) % 360
            angle_diff = (target_angle - player_angle + 180) % 360 - 180

            # Slowly adjust angle
            if abs(angle_diff) > 5:
                player_angle += angle_diff * 0.05

    # Auto-fire at enemies
    for enemy in enemies:
        dx = enemy.x - player_pos[0]
        dy = enemy.y - player_pos[1]
        angle_to_enemy = math.degrees(math.atan2(dy, dx)) % 360

        if abs((angle_to_enemy - player_angle + 180) % 360 - 180) < 15:
            if len(bullets) < 5 or random.random() < 0.1:
                bullet_x = player_pos[0] + 75 * math.cos(math.radians(player_angle))
                bullet_y = player_pos[1] + 75 * math.sin(math.radians(player_angle))
                bullet_z = player_pos[2] + 50  # Gun height
                bullets.append(Bullet(bullet_x, bullet_y, bullet_z, player_angle))

        break

def idle():
    if not game_over:
        update_bullets()
        update_enemies()
        check_obstacle_collision() # Check collision with obstacles
        cheat_mode_actions()
        if game_score >= LEVEL_SCORE_THRESHOLD * current_level:
            advance_level()
    glutPostRedisplay()

def advance_level():
    global current_level, game_score
    if current_level < 3:
        current_level += 1
        init_enemies()  # Initialize enemies for the new level
        init_obstacles() # Initialize obstacles for new level
        game_score = 0  # Reset score, or you can keep it
        print(f"Advancing to Level {current_level}!")  # For debugging
    #  else:
    #     print("Congratulations! You Win!") #commented out. the game continues even after level 3

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)

    setupCamera()

    draw_grid()
    draw_player()
    draw_hostage() #draw hostage
    draw_enemies()
    draw_bullets()
    draw_obstacles() # Draw obstacles

    draw_text(20, 770, f"Player Lives: {player_lives}")
    draw_text(20, 740, f"Game Score: {game_score}")
    draw_text(20, 710, f"Bullets Missed: {bullets_missed}")
    draw_text(20, 680, f"Level: {current_level}")
    draw_text(20, 650, f"Shields: {emergency_shields}")
    if shield_active:
        draw_text(20, 620, "Shield Active", GLUT_BITMAP_HELVETICA_12)

    if cheat_mode:
        draw_text(20, 680, "CHEAT MODE: ON", GLUT_BITMAP_HELVETICA_12)

    if game_over:
        draw_text(400, 400, "GAME OVER! Press R to restart", GLUT_BITMAP_TIMES_ROMAN_24)

    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Hostage Rescue Game")

    glEnable(GL_DEPTH_TEST)

    init_game()

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    glutMainLoop()

if __name__ == "__main__":
    main()
