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

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

light1_ambient = [0.1, 0.0, 0.3, 1.0]
light1_diffuse = [0.8, 0.0, 0.8, 1.0]
light1_specular = [1.0, 1.0, 1.0, 1.0]
light1_position = [0.0, 10.0, 0.0, 1.0]

LIGHT_AMBIENT = 0
LIGHT_DIFFUSE = 1
LIGHT_SPECTACULAR = 2

params = [light1_ambient, light1_diffuse, light1_specular]

selected_color_component = 0
selected_param = 0

phi = 0.0
mouse_y_pos_old = 0
delta_y = 0

right_mouse_button_pressed = 0

N = 40
x = lambda u, v: (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * math.cos(math.pi * v)
y = lambda u, v: 160 * u ** 4 - 320 * u ** 3 + 160 * u ** 2 - 5
z = lambda u, v: (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * math.sin(math.pi * v)

x_u = lambda u, v: (-450 * u ** 4 + 900 * u ** 3 - 810 * u ** 2 + 360 * u - 45) * math.cos(math.pi * v)
x_v = lambda u, v: math.pi * (90 * u ** 5 - 225 * u ** 4 + 270 * u ** 3 - 180 * u**2 + 45 * u) * math.sin(math.pi * v)
y_u = lambda u, v: 640 * u ** 3 - 960 * u ** 2 + 320 * u
y_v = lambda u, v: 0
z_u = lambda u, v: (-450 * u ** 4 + 900 * u ** 3 - 810 * u ** 2 + 360 * u - 45) * math.sin(math.pi * v)
z_v = lambda u, v: -math.pi * (90 * u ** 5 - 225 * u**4 + 270 * u ** 3 - 180 * u ** 2 + 45 * u) * math.cos(math.pi * v)

colors = np.random.rand(N, N, 3)

vertices = np.zeros((N, N, 3))
normal_vecs = np.zeros((N, N, 3))

u, v = np.linspace(0, 1, N), np.linspace(0, 1, N)

def normalize(vec):
    length = np.sqrt(vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2)
    return np.array([vec[0] / length, vec[1] / length, vec[2] / length])

for i in range(0, N):
    for j in range(0, N):
        vertices[i][j][0] = x(u[i], v[j])
        vertices[i][j][1] = y(u[i], v[j])
        vertices[i][j][2] = z(u[i], v[j])

        normal_vecs[i][j][0] = y_u(u[i], v[j]) * z_v(u[i], v[j]) - z_u(u[i], v[j]) * y_v(u[i], v[j])
        normal_vecs[i][j][1] = z_u(u[i], v[j]) * x_v(u[i], v[j]) - x_u(u[i], v[j]) * z_v(u[i], v[j])
        normal_vecs[i][j][2] = x_u(u[i], v[j]) * y_v(u[i], v[j]) - y_u(u[i], v[j]) * x_v(u[i], v[j])

        normal_vecs[i][j] = normalize(normal_vecs[i][j])
        normal_vecs[i][j] = -normal_vecs[i][j] if i >= N / 2 else normal_vecs[i][j]


def bajo_jajo():
    global vertices

    glBegin(GL_TRIANGLES)
    for i in range(N - 1):
        for j in range(N - 1):

            glNormal3fv(normal_vecs[i][j])
            glVertex3fv(vertices[i][j])

            glNormal3fv(normal_vecs[i + 1][j])
            glVertex3fv(vertices[i + 1][j])

            glNormal3fv(normal_vecs[i][j + 1])
            glVertex3fv(vertices[i][j + 1])

            # trójkąt dopełniający
            glNormal3fv(normal_vecs[i + 1][j + 1])
            glVertex3fv(vertices[i + 1][j + 1])

            glNormal3fv(normal_vecs[i + 1][j])
            glVertex3fv(vertices[i + 1][j])

            glNormal3fv(normal_vecs[i][j + 1])
            glVertex3fv(vertices[i][j + 1])

    glEnd()


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glLightfv(GL_LIGHT1, GL_AMBIENT, light1_ambient)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light1_diffuse)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light1_specular)
    glLightfv(GL_LIGHT1, GL_POSITION, light1_position)

    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    # glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)


def shutdown():
    pass

def draw_vectors():
    global normal_vecs

    glBegin(GL_LINES)
    for i in range(N):
        for j in range(N):
            glVertex3fv(vertices[i][j])
            glVertex3fv(vertices[i][j] + normal_vecs[i][j])

    glEnd()

def render(time):
    global theta
    global phi

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    theta %= 360
    phi %= 360

    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)

    # light1_position[0] = 13 * math.cos(theta * math.pi / 180) * math.cos(phi * math.pi / 180)
    # light1_position[1] = 13 * math.sin(phi * math.pi / 180)
    # light1_position[2] = 13 * math.sin(theta * math.pi / 180) * math.cos(phi * math.pi / 180)

    # glLightfv(GL_LIGHT1, GL_POSITION, light1_position)

    # glPushMatrix()
    # glTranslatef(light1_position[0], light1_position[1], light1_position[2])

    # quadric = gluNewQuadric()
    # gluQuadricDrawStyle(quadric, GLU_LINE)
    # gluSphere(quadric, 0.5, 6, 5)
    # gluDeleteQuadric(quadric)

    # glPopMatrix()

    # quadric = gluNewQuadric()
    # gluQuadricDrawStyle(quadric, GLU_FILL)
    # gluSphere(quadric, 3.0, 10, 10)
    # gluDeleteQuadric(quadric)

    bajo_jajo()

    if right_mouse_button_pressed:
        draw_vectors()

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
    global params
    global selected_param
    global selected_color_component

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if action == GLFW_PRESS or action == GLFW_REPEAT:
        if key == GLFW_KEY_A:
            selected_param = LIGHT_AMBIENT
        elif key == GLFW_KEY_D:
            selected_param = LIGHT_DIFFUSE
        elif key == GLFW_KEY_S:
            selected_param = LIGHT_SPECTACULAR
        elif key == GLFW_KEY_R:
            selected_color_component = 0
        elif key == GLFW_KEY_G:
            selected_color_component = 1
        elif key == GLFW_KEY_B:
            selected_color_component = 2
        elif key == GLFW_KEY_UP:
            params[selected_param][selected_color_component] = min(1.0, params[selected_param][selected_color_component] + 0.1)
        elif key == GLFW_KEY_DOWN:
            params[selected_param][selected_color_component] = max(0.0, params[selected_param][selected_color_component] - 0.1)
        
        if selected_param == LIGHT_AMBIENT:
            glLightfv(GL_LIGHT1, GL_AMBIENT, light1_ambient)
        elif selected_param == LIGHT_DIFFUSE:
            glLightfv(GL_LIGHT1, GL_DIFFUSE, light1_diffuse)
        elif selected_param == LIGHT_SPECTACULAR:
            glLightfv(GL_LIGHT1, GL_SPECULAR, light1_specular)

        print(f"Modyfikowanie: {selected_param} ({selected_color_component})")
        print(params)


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old
    global delta_y
    global mouse_y_pos_old

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
        right_mouse_button_pressed = not right_mouse_button_pressed


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