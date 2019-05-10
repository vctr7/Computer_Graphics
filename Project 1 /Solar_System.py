import glfw
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy as np

gCamAng = 0
gCamHeight = 1.

def drawCube():
    glBegin(GL_QUADS)
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f( 1.0,-1.0,-1.0)
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f( 1.0,-1.0,-1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f( 1.0,-1.0,-1.0)
    glEnd()

def drawSphere(numLats=12, numLongs=12):
    for i in range(0, numLats + 1):
        lat0 = np.pi * (-0.5 + float(float(i - 1) / float(numLats)))
        z0 = np.sin(lat0)
        zr0 = np.cos(lat0)
        lat1 = np.pi * (-0.5 + float(float(i) / float(numLats)))
        z1 = np.sin(lat1)
        zr1 = np.cos(lat1)
 # Use Quad strips to draw the sphere
        glBegin(GL_QUAD_STRIP)
        for j in range(0, numLongs + 1):
            lng = 2 * np.pi * float(float(j - 1) / float(numLongs))
            x = np.cos(lng)
            y = np.sin(lng)
            glVertex3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr1, y * zr1, z1)
        glEnd()


def drawTriangle():
    glColor3ub(255, 255, 255)
    glBegin(GL_TRIANGLES)
    glVertex3fv(np.array([.0,.5,0.]))
    glVertex3fv(np.array([.0,.0,0.]))
    glVertex3fv(np.array([.5,.0,0.]))
    glEnd()


    
def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 255, 255)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([5.,0.,0.]))
    glColor3ub(255, 255, 255)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,5.,0.]))
    glColor3ub(255, 255, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,2.]))
    glEnd()
    
def render(camAng, count):
    global gCamAng, gCamHeight
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glLoadIdentity()
    glOrtho(-1,1, -1,1, -8,8)
    gluLookAt(5*np.sin(gCamAng),gCamHeight,5*np.cos(gCamAng), 0,0,0, 0,1,0)

# Sun base transformation
    glPushMatrix()
# Sun base drawing
    glPushMatrix()
    glScalef(.1, .1, .1)
    glColor3ub(200, 0, 0)
    drawSphere()
    glPopMatrix()
    
# 지구
    glPushMatrix() #태양 중심
    glRotatef(count%360, 0.2, 1, 0) #태양 중심 회전
    glTranslatef(.7, 0, .01) #태양으로 부터 거리 0.5
# 지구
    glPushMatrix()
    glScalef(.05, .05, .05)
    glColor3ub(110, 117, 248)
    drawSphere()
    glPopMatrix()
#다시 태양 중심


    glPushMatrix() # 다시 지구 중심
    glRotatef(count%360, 1, 1, 0)
    glTranslatef(.1, 0, .0) #지구로부터 거리 0.2
# 달 그리기
    glPushMatrix()
    glScalef(.02, .02, .02) #달 크기
    glColor3ub(140, 140, 140)   #달 색깔 
    drawSphere()
    glPopMatrix()
#지구중심
    glPopMatrix()
    glPushMatrix() # 다시 지구 중심
    glTranslatef(-.5+(count%360)*.03, 0, 0)
    glPushMatrix()
    glScalef(.01, .012, .03) #로켓 크기
    glColor3ub(200, 200, 200)   #로켓 색깔 
    drawCube()
    glPopMatrix()
    
    glPopMatrix()

    
#태양중심
    glPopMatrix()
#수성 그리기
    glPushMatrix()
    glRotatef(count%360, 0.5, 1, 0.1) #태양 중심 회전
    glTranslatef(.2, 0, .01) #태양으로 부터 거리 0.2
    
    glPushMatrix()
    glScalef(.024, .024, .024) #수성 크기
    glColor3ub(186, 140, 94)   #수성 색깔 
    drawSphere()
    

    glPopMatrix()
    #혜성
    glPushMatrix()
    
    glRotatef(count%360, 0, 1, 0) #수성 중심 회전
    glTranslatef(1., 0, .01) #수성으로 부터 거리 1
    glPushMatrix()
    glScalef(.012, .012, .024) #수성 크기
    glColor3ub(255, 255, 255)   #수성 색깔
    drawSphere()
    glPopMatrix()
    #혜성 주위 인공위성
    glPushMatrix()
    
    glRotatef(count%360, 0, 1, 0) #수성 중심 회전
    glTranslatef(0.05, 0, .0) #수성으로 부터 거리 1
    glPushMatrix()
    glScalef(.0061, .0061, .012) #인공위성 크기
    glColor3ub(255, 255, 200)   #인공위성 색깔
    drawCube()

    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
#금성 그리기
    glPushMatrix()
    glRotatef(count%360, 0.2, 1, 0.2) #태양 중심 회전
    glTranslatef(.4, 0, .01) #태양으로 부터 거리 0.2
    
    glPushMatrix()
    glScalef(.049, .049, .049) #금성 크기
    glColor3ub(236, 227, 44)   #금성 색깔 
    drawSphere()
    glPopMatrix()
    glPopMatrix()

#화성 그리기
    glPushMatrix()
    glRotatef(count%360, 0.1, 1, 0.4) #태양 중심 회전
    glTranslatef(1, 0, .01) #태양으로 부터 거리 0.2
    
    glPushMatrix()
    glScalef(.03, .03, .03) #화성 크기
    glColor3ub(216, 107, 64)   #화성 색깔 
    drawSphere()
    glPopMatrix()
#화성 위성s
    glPushMatrix()
    glRotatef(count%360, 0, 1, 0) #화성 중심 회전
    glTranslatef(0.05, 0, .01) #화성으로 부터 거리 0.2
    
    glPushMatrix()
    glScalef(.01, .01, .01) #화성위성 1 크기
    glColor3ub(151, 129, 142)   #화성 색깔 
    drawSphere()
    glPopMatrix()
    glPopMatrix()
    glPushMatrix()
    glRotatef(count%360, 1.5, 1, 0) #화성 중심 회전
    glTranslatef(0.05, 0, .01) #화성으로 부터 거리 0.2
    glPushMatrix()
    glScalef(.008, .008, .008) #화성위성 2 크기
    glColor3ub(125, 102, 115)   #화성 색깔 
    drawSphere()
    glPopMatrix()
    
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
    global gCamAng, gCamHeight
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1


def main():
    if not glfw.init():
        return
    window = glfw.create_window(640, 640,'2014001321', None,None)
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
        count += 1.2
    glfw.terminate()
if __name__ == "__main__":
    main()

