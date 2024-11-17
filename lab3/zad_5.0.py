#!/usr/bin/env python3
import sys, math
import numpy as np

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()

def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)

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
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time * 180 / math.pi)

    axes()
    sierpinski_trujkont_czyde(0.0, 0.0, 0.0, 9.0, 5)

    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
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