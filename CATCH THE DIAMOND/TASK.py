import random
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import os

# Constants for window dimensions
WINDOW_WIDTH, WINDOW_HEIGHT = 400, 700

# Global variables
diamond_instance = None
catcher_instance = None
score_counter = 0
is_game_active = True
play_pause_status = "Pause"
is_diamond_caught = False
diamond_fall_rate = 0.008


# Diamond class definition
class Diamond:
    size = 0.02

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.points = self.calculate_points()
        self.color = self.random_color()

    def calculate_points(self):
        return [
            [self.x, self.y],
            [self.x + 1.5 * Diamond.size, self.y - 3 * Diamond.size],
            [self.x, self.y - 6 * Diamond.size],
            [self.x - 1.5 * Diamond.size, self.y - 3 * Diamond.size],
        ]

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.points = self.calculate_points()

    def random_color(self):
        return (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))


# Catcher class definition
class Catcher:
    size = 0.1

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.points = self.calculate_points()
        self.color = (1, 1, 1)

    def calculate_points(self):
        return [
            [self.x, self.y],
            [self.x + 5 * Catcher.size, self.y],
            [self.x + 0.1 + 3 * Catcher.size, self.y - 0.5 * Catcher.size],
            [self.x + 0.1, self.y - 0.5 * Catcher.size],
        ]

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.points = self.calculate_points()

    def reset_color(self):
        self.color = (1, 1, 1)


# Shape class definition for buttons
class Shape:
    def __init__(self, shape_type):
        self.points = []
        self.type = shape_type
        self.color = self.set_shape_points_and_color()

    def set_shape_points_and_color(self):
        if self.type == 'Restart':
            self.points = [[[-0.9, 0.8], [-0.7, 0.8]]]
            self.points.append([[-0.9, 0.8], [-0.8, 0.85]])
            self.points.append([[-0.9, 0.8], [-0.8, 0.75]])
            return (0, 128 / 255, 128 / 255)

        elif self.type == 'Pause':
            self.points = [[[-0.05, 0.75], [-0.05, 0.85]]]
            self.points.append([[0.05, 0.75], [0.05, 0.85]])
            return (1, 1, 0)

        elif self.type == 'Play':
            self.points = [[[-0.05, 0.75], [-0.05, 0.85]]]
            self.points.append([[-0.05, 0.75], [0.1, 0.8]])
            self.points.append([[-0.05, 0.85], [0.1, 0.8]])
            return (1, 1, 0)

        elif self.type == 'Cross':
            self.points = [[[0.75, 0.85], [0.85, 0.75]]]
            self.points.append([[0.75, 0.75], [0.85, 0.85]])
            return (1, 0, 0)


# Coordinate conversion function
def convert_coordinate(x, y):
    global WINDOW_WIDTH, WINDOW_HEIGHT
    x_cor = (2 * x - WINDOW_WIDTH) / WINDOW_WIDTH
    y_cor = (WINDOW_HEIGHT - 2 * y) / WINDOW_HEIGHT
    return [x_cor, y_cor]


# Midpoint Line Drawing Algorithm (Bresenham's Line Algorithm)
def midpoint_line_draw(start, end):
    """Bresenham's Line Algorithm to draw a line from start to end."""
    points = []
    x1, y1 = start
    x2, y2 = end
    
    dx = x2 - x1
    dy = y2 - y1
    sx = 1 if dx > 0 else -1
    sy = 1 if dy > 0 else -1
    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        err = dx / 2.0
        while x1 != x2:
            points.append([x1, y1])
            err -= dy
            if err < 0:
                y1 += sy
                err += dx
            x1 += sx
    else:
        err = dy / 2.0
        while y1 != y2:
            points.append([x1, y1])
            err -= dx
            if err < 0:
                x1 += sx
                err += dy
            y1 += sy
            
    points.append([x1, y1])  # Add the last point
    return points


# Drawing function for shapes
def draw_line(p1, p2, obj):
    points = midpoint_line_draw(p1, p2)
    glPointSize(2)
    glBegin(GL_POINTS)
    glColor3f(*obj.color)
    for point in points:
        glVertex2d(point[0], point[1])
    glEnd()


# Diamond falling logic
def diamond_fall():
    global diamond_instance, catcher_instance, is_diamond_caught, score_counter, diamond_fall_rate, play_pause_status
    d1 = diamond_instance
    fall_rate = diamond_fall_rate if is_game_active and play_pause_status != 'Play' else 0

    if d1.points[3][1] >= -0.80:
        d1.set_position(d1.x, d1.y - fall_rate)
    else:
        d1.set_position(random.uniform(-0.75, 0.75), 0.75)
        is_diamond_caught = False

    glutPostRedisplay()


# Catcher movement handling
def catcher_move(key, x, y):
    global catcher_instance, play_pause_status
    c1 = catcher_instance
    step_size = 0.08 if is_game_active else 0

    if play_pause_status == "Pause" and is_game_active:
        step_size = 0.08

    if play_pause_status == "Play":
        step_size = 0

    if key == GLUT_KEY_LEFT and c1.x > -1:
        c1.set_position(c1.x - step_size, c1.y)
    elif key == GLUT_KEY_RIGHT and c1.x + 0.5 < 1:
        c1.set_position(c1.x + step_size, c1.y)

    glutPostRedisplay()


# Drawing the shapes
def draw_shape(obj):
    for i in range(len(obj.points)):
        draw_line(obj.points[i % len(obj.points)], obj.points[(i + 1) % len(obj.points)], obj)


def draw_button(obj):
    for i in range(len(obj.points)):
        draw_line(obj.points[i][0], obj.points[i][1], obj)


# Game initialization
def game_init():
    global diamond_instance, catcher_instance
    diamond_instance = Diamond(random.uniform(-0.75, 0.75), 0.60)
    catcher_instance = Catcher(random.uniform(-1, 0.5), -0.85)


def mouse_handler(btn, state, x, y):
    global play_pause_status, is_game_active, score_counter, is_diamond_caught, diamond_fall_rate, diamond_instance, catcher_instance
    if btn == GLUT_LEFT_BUTTON:
        if state == GLUT_UP:
            x, y = convert_coordinate(x, y)
            # Handle pause button
            if -0.05 < x < 0.05 and 0.75 < y < 0.85:
                play_pause_status = 'Play' if play_pause_status == 'Pause' else 'Pause'
                print(f"Game is now {play_pause_status}.")
                
            # Handle exit button
            elif 0.75 < x < 0.85 and 0.75 < y < 0.85:
                print(f"Exiting game with final score: {score_counter}.")
                os._exit(0)
                
            # Handle restart button
            elif -0.9 < x < -0.7 and 0.75 < y < 0.85 and play_pause_status == 'Pause':
                print("Game restarting...")
                score_counter = 0
                is_game_active = True
                play_pause_status = "Pause"
                is_diamond_caught = False
                diamond_fall_rate = 0.008
                diamond_instance = Diamond(random.uniform(-0.75, 0.75), 0.60)
                catcher_instance = Catcher(catcher_instance.x, catcher_instance.y)


def show_stuff():
    global diamond_instance, catcher_instance, score_counter, is_game_active, is_diamond_caught, diamond_fall_rate, play_pause_status
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    
    play_n_pause = Shape(play_pause_status)
    cross = Shape('Cross')
    restart = Shape('Restart')

    draw_button(play_n_pause)
    draw_button(cross)
    draw_button(restart)

    d1 = diamond_instance
    c1 = catcher_instance

    if not is_diamond_caught and d1.points[2][1] <= c1.y and is_game_active:
        if d1.points[2][0] <= c1.points[0][0] or d1.points[2][0] > c1.points[1][0]:
            is_game_active = False
            c1.reset_color()  # Change catcher color to red
            print(f"Game Over! Final score: {score_counter}")
        else:
            score_counter += 1
            is_game_active = True
            print(f"Score: {score_counter}")
            d1.random_color()
            diamond_fall_rate += 0.002  
        is_diamond_caught = True
    
    draw_shape(catcher_instance)
    if is_game_active:
        draw_shape(diamond_instance)
    
    glutSwapBuffers()


def start():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1, 1, -1, 1)
    game_init()


# OpenGL setup
glutInit()
glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"CATCH THE DIAMOND")

start()

# Register callbacks
glutDisplayFunc(show_stuff)
glutIdleFunc(diamond_fall)
glutSpecialFunc(catcher_move)
glutMouseFunc(mouse_handler)
glutMainLoop()
