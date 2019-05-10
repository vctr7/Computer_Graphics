import glfw
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy as np

gCamAng = 0

def drawTriangleTransformedBy(M):
    glColor3ub(255, 255, 255)
    glBegin(GL_TRIANGLES)
    glVertex3fv((M @ np.array([.0,.5,0.,1.]))[:-1])
    glVertex3fv((M @ np.array([.0,.0,0.,1.]))[:-1])
    glVertex3fv((M @ np.array([.5,.0,0.,1.]))[:-1])
    glEnd()
def drawTriangle():
    glColor3ub(255, 255, 255)
    glBegin(GL_TRIANGLES)
    glVertex3fv(np.array([.0,.5,0.]))
    glVertex3fv(np.array([.0,.0,0.]))
    glVertex3fv(np.array([.5,.0,0.]))
    glEnd()

def drawFrameTransformedBy1(M):
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv( (M @ np.array([0.,0.,0.,1.]))[:-1] )
    glVertex3fv( (M @ np.array([1.,0.,0.,1.]))[:-1] )
    glColor3ub(0, 255, 0)
    glVertex3fv( (M @ np.array([0.,0.,0.,1.]))[:-1] )
    glVertex3fv( (M @ np.array([0.,1.,0.,1.]))[:-1] )
    glColor3ub(0, 0, 255)
    glVertex3fv( (M @ np.array([0.,0.,0.,1.]))[:-1] )
    glVertex3fv( (M @ np.array([0.,0.,1.,1.]))[:-1] )
    glEnd()
    
def drawFrameTransformedBy2(M):
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(M[:3,3]) # origin point
    glVertex3fv(M[:3,3] + M[:3,0]) # origin point + x axis vector
    glColor3ub(0, 255, 0)
    glVertex3fv(M[:3,3]) # origin point
    glVertex3fv(M[:3,3] + M[:3,1]) # origin point + y axis vector
    glColor3ub(0, 0, 255)
    glVertex3fv(M[:3,3]) # origin point
    glVertex3fv(M[:3,3] + M[:3,2]) # origin point + z axis vector
    glEnd()
    
def drawFrame():
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
    
def render(camAng, count):
    global gCamAng
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glLoadIdentity()
    glOrtho(-1,1, -1,1, -1,1)
    gluLookAt(.1*np.sin(camAng), .1,.1*np.cos(camAng), 0,0,0, 0,1,0)
    
##############################
# edit here
# draw the global frame
    drawFrame()
# blue base transformation
    glPushMatrix()
    glTranslatef(-.5+(count%360)*.003, 0, 0)
# blue base drawing
    glPushMatrix()
    drawFrame()

    glScalef(.2, .2, .2)
    glColor3ub(0, 0, 255)
    drawBox()
    glPopMatrix()
# red arm transformation
    glPushMatrix()
    glRotatef(count%360, 0, 0, 1)
    glTranslatef(.5, 0, .01)
# red arm drawing
    glPushMatrix()
    drawFrame()
    glScalef(.5, .1, .1)
    glColor3ub(255, 0, 0)
    drawBox()
    glPopMatrix()
    glPopMatrix()
    
    # green base transformation
    glPushMatrix()
    glRotatef(count%360, 0, 0, 1)
    glTranslatef(1, 0, .01)

    # green base drawing
    glPushMatrix()
    drawFrame()
    glRotatef(count%360, 0, 0, 1)

    glScalef(.15, .15, .15)
    glColor3ub(0, 255, 0)
    drawBox()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()

def drawBox():
    glBegin(GL_QUADS)
    glVertex3fv(np.array([1,1,0.]))
    glVertex3fv(np.array([-1,1,0.]))
    glVertex3fv(np.array([-1,-1,0.]))
    glVertex3fv(np.array([1,-1,0.]))
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
    global gCamAng
    if not glfw.init():
        return
    window = glfw.create_window(640,640,'Lecture9', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.swap_interval(1)

    count = 0
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render(gCamAng, count)
        glfw.swap_buffers(window)
        count += 1
    glfw.terminate()
if __name__ == "__main__":
    main()

