#!/usr/bin/env python3
import sys, math

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

def draw_triangle(x: float, y: float, a: float) -> None:
    """Rysuje trójkąt równoboczny"""
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(x, y)
    glVertex2f(x + a, y)
    glVertex2f(x + a / 2, y + a * math.sqrt(3) / 2)
    glEnd()

def draw_trujkont_sierpinskiego(x: float, y: float, a: float, depth: int) -> None:
    """Rysuje trujkont Sierpińskiego"""
    if depth == 0:
        # jak rekurencja dobije do końca to rysuje trujkonta
        draw_triangle(x, y, a)
    else:
        # wyższa matma
        # taka licealna
        # musiałem wygooglać wzór na wysokość trójkąta boże
        draw_trujkont_sierpinskiego(x, y, a / 2, depth - 1)
        draw_trujkont_sierpinskiego(x + a / 2, y, a / 2, depth - 1)
        draw_trujkont_sierpinskiego(x + a / 4, y + a * math.sqrt(3) / 4, a / 2, depth - 1)




def render(time):
    draw_trujkont_sierpinskiego(-50.0, -50.0, 90.0, 4)


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
