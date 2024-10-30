#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass

def draw_rectangle(x: float, y: float, a: float, b: float, d: float = 0.0) -> None:
    # glClear(GL_COLOR_BUFFER_BIT)

    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(x + d, y + d)
    glVertex2f(x + a + d, y + d)
    glVertex2f(x + d, y + b + d)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(x + a + d, y + b + d)
    glVertex2f(x + a + d, y + d)
    glVertex2f(x + d, y + b + d)
    glEnd()

    glFlush()

def draw_dywan(x: float, y: float, a: float, depth: int) -> None:
    """Rysuje dywan Sierpińskiego"""
    if depth == 0:
        # jak rekurencja dobije do końca to rysuje kwadrata
        draw_rectangle(x, y, a, a)
    else:
        # dzielimy na małe kwadraciki
        for i in range(3):
            for j in range(3):
                if i == 1 and j == 1:
                    continue # dziura na środku
                draw_dywan(x + i * a / 3, y + j * a / 3, a / 3, depth - 1)



def render(time):
    draw_dywan(-50.0, -50.0, 90.0, 4)


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
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

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
