import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

gCamAng = 0.

def myLookAt(eye,at,up):
    w = (eye-at)/np.sqrt(np.dot(eye-at,eye-at))
    u = np.cross(up, w)/np.sqrt(np.dot(np.cross(up, w), np.cross(up,w)))
    v = np.cross(w, u)
    
    M= np.array([[u[0], u[1], u[2], -np.dot(u, eye)],
                 [v[0], v[1], v[2], np.dot(-v, eye)],
                 [w[0], w[1], w[2], np.dot(-w, eye)],
                 [0, 0, 0, 1]])

    glMultMatrixf(M.T)

def myOrtho(l, r, b, t, n, f):
    Morth = np.array([[2/(r-l),0 , 0,-(r+l)/(r-l)],
                     [ 0, 2/(t-b), 0, -(t+b)/(t-b)],
                     [ 0, 0, -2/(f-n), -(f+n)/(f-n)],
                     [ 0, 0, 0, 1]])
    
def render(camAng):
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
# set the current matrix to the identity matrix
    glLoadIdentity()
# use orthogonal projection (right-multiply the current matrix by "projection" matrix - we'll see details later)


    myOrtho(left, right, bottom, top, near, far)
    #glOrtho(-1,1, -1,1, -10,10)
    
# rotate "camera" position (right-multiply the current matrix by viewing matrix)
# try to change parameters

    eye = np.array([1*np.sin(camAng),.5,1*np.cos(camAng)])
    up = np.array([0, 1, 0])
    at = np.array([0, 0, 0])
    myLookAt(eye, at, up)

   
    myOrtho()
    

# draw coordinates
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global gCamAng
# rotate the camera when 1 or 3 key is pressed or repeated
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)

def main():
    if not glfw.init():
        return
    window = glfw.create_window(640,640,'Lecture8', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render(gCamAng)
        glfw.swap_buffers(window)
    glfw.terminate()
if __name__ == "__main__":
    main()
