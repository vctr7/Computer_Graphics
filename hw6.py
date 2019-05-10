import glfw
from OpenGL.GLU import *
from OpenGL.GL import *

import numpy as np



def key_callback(window, key, scancode, action, mods):
    global T, camAng, count
    
    if key==glfw.KEY_Q:
        if action==glfw.PRESS:
            
            T =  np.array([[1, 0, 0, -0.1], [0.,1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]) @ T
                
            
    if key==glfw.KEY_E:
        if action==glfw.PRESS:
            T =  np.array([[1, 0, 0, 0.1], [0.,1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]) @ T
            
    if key==glfw.KEY_A:
        if action==glfw.PRESS:
            th = np.radians(-10)
            T = T @ np.array([[np.cos(th),0., np.sin(th),0.],
                      [0., 1, 0 ,0.],
                      [-np.sin(th), 0, np.cos(th),0.],
                      [0.,0.,0.,1.]])
            
    if key==glfw.KEY_D:
        if action==glfw.PRESS:
            th = np.radians(10)

            T = T @ np.array([[np.cos(th),0., np.sin(th),0.],
                      [0., 1, 0 ,0.],
                      [-np.sin(th), 0, np.cos(th),0.],
                      [0.,0.,0.,1.]])
            
    if key==glfw.KEY_W:
        if action==glfw.PRESS:
            th = np.radians(-10)
            
            T = T @ np.array([[1.,0.,0.,0.],
                      [0., np.cos(th), np.sin(th),0.],
                      [0., -np.sin(th), np.cos(th),0.],
                      [0.,0.,0.,1.]])
    if key==glfw.KEY_S:
        if action==glfw.PRESS:
            th = np.radians(10)
            T = T @ np.array([[1.,0.,0.,0.],
                      [0., np.cos(th), np.sin(th),0.],
                      [0., -np.sin(th), np.cos(th),0.],
                      [0.,0.,0.,1.]])
            
    if key==glfw.KEY_1:
        if action==glfw.PRESS:
            camAng += np.radians(10)

    if key==glfw.KEY_3:
        if action==glfw.PRESS:
            camAng += np.radians(-10)
            
            
def drawTriangle():
    glColor3ub(255, 255, 255)
    glBegin(GL_TRIANGLES)
    glVertex3fv(np.array([.0,.5,0.]))
    glVertex3fv(np.array([.0,.0,0.]))
    glVertex3fv(np.array([.5,.0,0.]))
    glEnd()


def render(M, camAng):
    
    # enable depth test (we'll see details later)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glLoadIdentity()
    
    # use orthogonal projection (we'll see details later)
    glOrtho(-1,1, -1,1, -1,1)
    
    # rotate "camera" position to see this 3D space better (we'll see details later)
    gluLookAt(.1*np.sin(camAng),.1,.1*np.cos(camAng), 0,0,0, 0,1,0)

    # draw coordinate: x in red, y in green, z in blue
    glBegin(GL_LINES)
    #x
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    #y
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    #z
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()

    glMultMatrixf(M.T)
    drawTriangle()


def main():


    global T, camAng, count
    count = 0
    camAng = np.radians(count % 360)
    
    T = np.array([[1,0, 0, 0],[0,1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    
    if not glfw.init():
        return

    window = glfw.create_window(480, 480, "2014001321", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    while not glfw.window_should_close(window):
        glfw.poll_events()

        
        glfw.set_key_callback(window, key_callback)
        render(T, camAng)

        glfw.swap_buffers(window)


    glfw.terminate()

if __name__ == "__main__":
    main()

