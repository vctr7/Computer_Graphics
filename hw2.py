import glfw
import numpy as np
from OpenGL.GL import *


def key_callback(window, key, scancode, action, mods):
    global pr
    if key==glfw.KEY_1:
        if action==glfw.PRESS:
            pr = GL_POINTS
    if key==glfw.KEY_2:
        if action==glfw.PRESS:
            pr = (GL_LINES)
    if key==glfw.KEY_3:
        if action==glfw.PRESS:
            pr = (GL_LINE_STRIP)
    if key==glfw.KEY_4:
        if action==glfw.PRESS:
            pr = (GL_LINE_LOOP)
    if key==glfw.KEY_5:
        if action==glfw.PRESS:
            pr = (GL_TRIANGLES)
    if key==glfw.KEY_6:
        if action==glfw.PRESS:
            pr = (GL_TRIANGLE_STRIP)
    if key==glfw.KEY_7:
        if action==glfw.PRESS:
            pr = (GL_TRIANGLE_FAN)
    if key==glfw.KEY_8:
        if action==glfw.PRESS:
            pr = (GL_QUADS)
    if key==glfw.KEY_9:
        if action==glfw.PRESS:
            pr = (GL_QUAD_STRIP)
    if key==glfw.KEY_0:
        if action==glfw.PRESS:
            pr = (GL_POLYGON)
    
def render():
    global pr
    x = np.linspace(0, 2*np.pi, 13)[:-1]

    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(pr)

    #glBegin(GL_POINTS)
    #glBegin(GL_LINES)
    #glBegin(GL_LINE_STRIP)
    #glBegin(GL_LINE_LOOP)

    for i in range(12):

        glVertex2f(np.cos(x[i]),np.sin(x[i]))
        
    glEnd()

def main():


    global pr
    pr = GL_LINE_LOOP
    if not glfw.init():
        return

    window = glfw.create_window(480, 480, "2014001321", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        render()

        glfw.swap_buffers(window)


    glfw.terminate()

if __name__ == "__main__":
    main()

