###############################
# page 27
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.arrays import vbo
import ctypes
import os
import sys

gCamAng = 0.
gCamHeight = 1.
gZoom = 120
flag = False
gPolygonFlag = False

def render(ang):
    global gCamAng, gCamHeight, gZoom
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION) # use projection matrix stack for projection transformation for correct lighting
    glLoadIdentity()
    gluPerspective(gZoom, 1, 1,10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(5*np.sin(gCamAng),gCamHeight,5*np.cos(gCamAng), 0,0,0, 0,1,0)

    drawFrame()

    glEnable(GL_LIGHTING)   # try to uncomment: no lighting
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT3)

    # light position
    glPushMatrix()

    glRotatef(ang,0,1,0)  # try to uncomment: rotate light
    lightPos = (20.,10.,8.,1)    # try to change 4th element to 0. or 1.
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)

    glPopMatrix()


    # light intensity for each color channel
    ambientLightColor = (1,.384,0,1.)
    diffuseLightColor = (0.85,0.85,0.85,1.)
    specularLightColor = (1.,0.384,0.,1.)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specularLightColor)



    # material reflectance for each color channel
    diffuseObjectColor = (0.85,0.85,0.85)
    specularObjectColor = (0.85,0.85,0.85,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, diffuseObjectColor)
    #glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    glPushMatrix()
    # glRotatef(ang,0,1,0)    # try to uncomment: rotate object

    glColor3ub(13, 13, 13) # glColor*() is ignored if lighting is enabled

    # drawUnitCube_glVertex()
    if flag == True:
        drawUnitCube_glDrawElements()

    glPopMatrix()

    glDisable(GL_LIGHTING)

def drawUnitCube_glDrawElements():
    global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed #vertex
    iarr = gIndexArray #face
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, 3*varr.itemsize, varr)
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)
   

   
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

def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight, gZoom, gPolygonFlag
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1
        elif key==glfw.KEY_A:
            gZoom += -1
        elif key==glfw.KEY_S:
            gZoom += 1
        elif key==glfw.KEY_Z:
            gPolygonFlag = not gPolygonFlag
            if gPolygonFlag == 1:
                glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
            elif gPolygonFlag == 0:
                glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )

def filterFace(face):
    t1 = []
    t2 = []
    new = []

    for i in face:
        t1 = []
        for j in i:
            t2 = []
            t2 = int(j[:j.index('/')])-1
            t1.append(t2)
        new.append(t1)

    return new        

def drop_callback(window, paths):
    vertex = []
    vertex_normal = []
    face = []
    global gVertexArrayIndexed, gIndexArray, flag
    face_triangle= []
    face_quads = []
    three_vertex = 0
    four_vertex = 0
    much_vertex = 0
    file = open(paths[0])
    lines=0
    i = 0
    for line in file:
        
        if line[:2] == "vn":
            vertex_normal.append(list(tuple(float(vn) for vn in line[3:].strip().split(' '))))
            
        elif line[0] == "v":
            vertex.append(list(tuple(float(v) for v in line[2:].strip().split(' '))))

        elif line[0] == "f":
            lines+=1
            face.append(list(tuple(line[2:].strip().split(' '))))            
            if len(face[len(face)-1]) == 3 :
                three_vertex += 1
                face_triangle.append(list(tuple(line[2:].strip().split(' '))))
                
            elif len(face[len(face)-1]) == 4 :
                four_vertex += 1
                face_quads.append(list(tuple(line[2:].strip().split(' '))))
                
            else :
                much_vertex += 1
                face_quads.append(list(tuple(line[2:].strip().split(' '))))
                
    face = filterFace(face)
    file.close()

    filename = os.path.split(paths[0])

    print("Information of obj file")
    print("File name :", filename[1])
    print("Total number of faces :", lines)
    print("Number of faces with 3 vertices :", three_vertex)
    print("Number of faces with 4 vertices :", four_vertex)
    print("Number of faces with more than 4 vertices :", much_vertex)
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass    
    
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass
        
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass
                                                                                                        
    for i in face:
        j=i
        if len(i)==4:
            s = i.pop()
            face.append([i[0], i[2], s])
            
        elif len(i) > 4:
            s1 = i.pop()
            for n in j:
                s2 = i.pop()
                face.append([i[0], s2, s1])
                s1 = s2   
        else:
            pass
    varr = np.array(vertex, 'float32')
    iarr = np.array(face)
    gVertexArrayIndexed = varr
    gIndexArray = iarr
    flag = True
    

def main():
    global gVertexArraySeparate, gVertexArrayIndexed, gIndexArray

    if not glfw.init():
        return
    window = glfw.create_window(640,640,'OBJViewer', None,None)

    if not window:
    
        glfw.terminate()
        return
    glfw.set_drop_callback(window, drop_callback)
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.swap_interval(1)


    count = 300
    while not glfw.window_should_close(window):
        glfw.poll_events()
        ang = count % 360
        render(ang)
        count += 1
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
			
