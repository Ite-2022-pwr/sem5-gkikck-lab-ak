#!/usr/bin/env python3
import sys, math, numpy as np

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


viewer = [0.0, 0.0, 10.0]

theta = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0

phi = 0.0
mouse_y_pos_old = 0
delta_y = 0

right_mouse_button_pressed = 0
scale = 1.0

R = 10.0

X_key_pressed = 0

W_key_pressed = 0
A_key_pressed = 0
S_key_pressed = 0
D_key_pressed = 0

i_like_to_move_it_move_it = [0.0, 0.0, 0.0]

mouse_moved = 0

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-50.0, 0.0, 0.0)
    glVertex3f(50.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -50.0, 0.0)
    glVertex3f(0.0, 50.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -50.0)
    glVertex3f(0.0, 0.0, 50.0)

    glEnd()


def example_object():
    glColor3f(1.0, 1.0, 1.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    glRotatef(90, 1.0, 0.0, 0.0)
    glRotatef(-90, 0.0, 1.0, 0.0)

    gluSphere(quadric, 1.5, 10, 10)

    glTranslatef(0.0, 0.0, 1.1)
    gluCylinder(quadric, 1.0, 1.5, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, -1.1)

    glTranslatef(0.0, 0.0, -2.6)
    gluCylinder(quadric, 0.0, 1.0, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, 2.6)

    glRotatef(90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(-90, 1.0, 0.0, 1.0)

    glRotatef(-90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(90, 1.0, 0.0, 1.0)

    glRotatef(90, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gluDeleteQuadric(quadric)


def draw_pyramid(x, y, z, a):
    glBegin(GL_TRIANGLES)

    # ściana 1
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(x, y, z)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(x + a, y, z)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(x + a / 2, y + a * math.sqrt(3) / 2, z + a * math.sqrt(3) / 6)

    # ściana 2
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(x, y, z)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(x + a, y, z)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(x + a / 2, y, z + a * math.sqrt(3) / 2)

    # ściana 3
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(x, y, z)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(x + a / 2, y, z + a * math.sqrt(3) / 2)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(x + a / 2, y + a * math.sqrt(3) / 2, z + a * math.sqrt(3) / 6)

    # ściana 4
    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(x + a, y, z)
    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(x + a / 2, y, z + a * math.sqrt(3) / 2)
    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(x + a / 2, y + a * math.sqrt(3) / 2, z + a * math.sqrt(3) / 6)

    glEnd()


def sierpinski_trujkont_czyde(x, y, z, a, depth=0):
    if depth == 0:
        draw_pyramid(x, y, z, a)
    else:
        sierpinski_trujkont_czyde(x, y, z, a / 2, depth - 1)
        sierpinski_trujkont_czyde(x + a / 2, y, z, a / 2, depth - 1)
        sierpinski_trujkont_czyde(x + a / 4, y, z + a *math.sqrt(3) / 4, a / 2, depth - 1)
        sierpinski_trujkont_czyde(x + a / 4, y + a *math.sqrt(3) / 4, z + a *math.sqrt(3) / 12, a / 2, depth - 1)


def render(time):
    global theta
    global phi
    global scale
    global R
    global mouse_moved

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    theta %= 360
    phi %= 360

    x_eye = R * math.cos(theta * math.pi / 180) * math.cos(phi * math.pi / 180)
    y_eye = R * math.sin(phi * math.pi / 180)
    z_eye = R * math.sin(theta * math.pi / 180) * math.cos(phi * math.pi / 180)

    rot = -1.0 if phi > 90 and phi < 270 else 1.0

    gluLookAt(viewer[0] + i_like_to_move_it_move_it[0], viewer[1] + i_like_to_move_it_move_it[1], viewer[2] + i_like_to_move_it_move_it[2], viewer[0] + i_like_to_move_it_move_it[0] + x_eye, viewer[1] + i_like_to_move_it_move_it[1] + y_eye, viewer[2] + i_like_to_move_it_move_it[2] + z_eye, 0.0, rot, 0.0)

    if mouse_moved:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle
    mouse_moved = False

    # glRotatef(theta, 0.0, 1.0, 0.0)
    # glRotatef(phi, 1.0, 0.0, 0.0)

    if right_mouse_button_pressed:
        scale += delta_y * 0.01
        R += delta_y * 0.1
        R = max(3.0, R)
        R = min(20.0, R)

    if W_key_pressed:
        i_like_to_move_it_move_it[0] += x_eye * 0.05
        i_like_to_move_it_move_it[1] += y_eye * 0.05
        i_like_to_move_it_move_it[2] += z_eye * 0.05
    if A_key_pressed:
        right = np.cross([x_eye, y_eye, z_eye], [0.0, 1.0, 0.0])
        i_like_to_move_it_move_it[0] -= right[0] * 0.05
        i_like_to_move_it_move_it[1] -= right[1] * 0.05
        i_like_to_move_it_move_it[2] -= right[2] * 0.05
    if S_key_pressed:
        i_like_to_move_it_move_it[0] -= x_eye * 0.05
        i_like_to_move_it_move_it[1] -= y_eye * 0.05
        i_like_to_move_it_move_it[2] -= z_eye * 0.05
    if D_key_pressed:
        right = np.cross([x_eye, y_eye, z_eye], [0.0, 1.0, 0.0])
        i_like_to_move_it_move_it[0] += right[0] * 0.05
        i_like_to_move_it_move_it[1] += right[1] * 0.05
        i_like_to_move_it_move_it[2] += right[2] * 0.05
   

    # glScalef(scale, scale, scale)

    axes()
    sierpinski_trujkont_czyde(0.0, 0.0, 0.0, 9.0, 5)

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global X_key_pressed
    global W_key_pressed
    global A_key_pressed
    global S_key_pressed
    global D_key_pressed

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_X and action == GLFW_PRESS:
        X_key_pressed = not X_key_pressed

    if action == GLFW_PRESS or action == GLFW_REPEAT:
        if key == GLFW_KEY_W:
            W_key_pressed = 1
        elif key == GLFW_KEY_S:
            S_key_pressed = 1
        elif key == GLFW_KEY_A:
            A_key_pressed = 1
        elif key == GLFW_KEY_D:
            D_key_pressed = 1
    else:
        W_key_pressed = 0
        A_key_pressed = 0
        S_key_pressed = 0
        D_key_pressed = 0


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old
    global delta_y
    global mouse_y_pos_old

    global mouse_moved
    mouse_moved = 1

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    global right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0

    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    else:
        right_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()