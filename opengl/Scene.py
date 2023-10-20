import pygame as pg
from pygame.locals import *
from OpenGL.GLU import *
from opengl.BoundingBox import *
from opengl.BackgroundPlane import *

class Scene:
    screen = None
    def __init__(self, args, width, height):        
        pg.init()
        pg.font.init()
        Scene.screen = pg.display.set_mode((width, height), DOUBLEBUF|OPENGL |OPENGLBLIT)
        self.clock = pg.time.Clock()
        self.zoom = 1
        self.initialZoom = 1
        self.panX = 0
        self.panY = 0
        self.width = width
        self.height = height
        self.args = args
        self.backGroundPlane = BackgroundPlane()
        self.viewport(width, height)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable( GL_BLEND )
        glDepthFunc(GL_ALWAYS)
        glDisable(GL_DEPTH_TEST)
    
    def pan(self, dx, dy):
        self.panX += dx*self.initialZoom
        self.panY += dy*self.initialZoom
        self.setup()
        self.updateVisibleWorldBoundingBox()
    
    def zoomBy(self, factor):
        if self.zoom*factor<100 and self.zoom*factor>0.01:
            self.zoom *= factor
            self.panX *= factor
            self.panY *= factor
            self.setup()
            self.updateVisibleWorldBoundingBox()
    
    def viewport(self, w, h):
        aspect = 1.0 * h / w
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        #gluOrtho2D(-w/2, w/2, -h/2, h/2)
        self.initialZoom = 10/self.height
        gluOrtho2D(-5/aspect, 5/aspect, -5, 5)
        self.updateVisibleWorldBoundingBox()
    
    def setup(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(self.panX, self.panY, 0)
        glScalef(self.zoom, self.zoom, 1)

    def animate(self):
        pass

    def keyPress(self, unicode, shift, ctrl):
        pass

    def mouseDrag(self, screenP, worldP, deltaScreen, deltaWorld, shift, crtl, alt):
        pass

    def mouseDragEnd(self, screenP, worldP, deltaScreen, deltaWorld):
        pass

    def mousePress(self, screenP, worldP):
        pass

    def mouseRelease(self, screenP, worldP, endDrag):
        pass

    def draw(self):
        pass
    
    def screen2world(self, p):
        x = ((p[0] - self.width/2)*self.initialZoom - self.panX)/self.zoom
        y = ((p[1] - self.height/2)*self.initialZoom+ self.panY)/self.zoom
        return np.array([x,-y])
    
    def updateVisibleWorldBoundingBox(self):
        minW = self.screen2world([0,self.height])
        maxW = self.screen2world([self.width,0])

        w = maxW[0]-minW[0]
        h = maxW[1]-minW[1]
        cx = (maxW[0]+minW[0])/2
        cy = (maxW[1]+minW[1])/2
        self.visibleWorldBoundingBox = BoundingBox(w, h, [cx, cy])
        self.backGroundPlane.updateBounds(self.visibleWorldBoundingBox)

    def loop(self):
        drag = False

        while True:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == K_ESCAPE:
                        pg.quit()
                        quit()
                    shift = event.mod & KMOD_SHIFT
                    ctrl = event.mod & KMOD_CTRL
                    code = event.unicode
                    if code=="":
                        code = event.scancode
                    self.keyPress(code, shift, ctrl)
                elif event.type == pg.MOUSEWHEEL:
                    self.zoomBy(event.y/10+1)
                elif event.type == pg.MOUSEBUTTONDOWN:                   
                    if event.button==1:
                        p = self.screen2world(event.pos)
                        self.mousePress(event.pos, p)
                elif event.type == pg.MOUSEMOTION:                   
                    if event.buttons[2]==1 or event.buttons[1]==1:
                        self.pan(event.rel[0], -event.rel[1])
                    elif event.buttons[0]==1:
                        pWorld = self.screen2world(event.pos)
                        relWorld = [event.rel[0]/self.zoom*self.initialZoom, -event.rel[1]/self.zoom*self.initialZoom]
                        shift = pg.key.get_mods() & KMOD_SHIFT
                        ctrl = pg.key.get_mods() & KMOD_CTRL
                        alt = pg.key.get_mods() & KMOD_ALT
                        self.mouseDrag(event.pos, pWorld, event.rel, relWorld, shift, ctrl, alt)
                        drag=True
                elif event.type == pg.MOUSEBUTTONUP:                    
                    p = self.screen2world(event.pos)
                    if drag:
                        self.mouseDragEnd(event.pos, p)
                        drag=False
                    else:
                        self.mouseRelease(event.pos, p)                    

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            
            self.animate()
            
            glPushMatrix()

            glPushAttrib(GL_LINE_BIT)
            glPushAttrib(GL_CURRENT_BIT)
            
            self.backGroundPlane.draw()
            
            glPopAttrib(GL_CURRENT_BIT)
            glPopAttrib(GL_LINE_BIT)

            self.draw()
            
            glPopMatrix()

            pg.display.flip()
            
            self.clock.tick(60)
   