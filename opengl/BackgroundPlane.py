from math import *
from OpenGL.GL import *

class BackgroundPlane:
    def __init__(self):        
        self.dx = 1
        self.planeTransition = 5
        self.minX = 0
        self.minY = 0
        self.maxX = 0
        self.maxY = 0
        self.minDx = 0
        self.maxDx = 0

    def updateBounds(self, wBB):

        minX = wBB.minX()
        maxX = wBB.maxX()
        minY = wBB.minY()
        maxY = wBB.maxY()

        maxDim = max(maxX-minX, maxY-minY)

        tmp = int(log(maxDim,self.planeTransition))-1

        dx = pow(self.planeTransition,tmp)

        self.dx = dx

        self.minX = (int(minX/dx)-1)*dx
        self.maxX = (int(maxX/dx)+1)*dx
        self.minY = (int(minY/dx)-1)*dx
        self.maxY = (int(maxY/dx)+1)*dx
       
        w = self.maxY-self.minY

        self.minDx = self.dx
        while w/self.minDx<10:
            self.minDx /= self.planeTransition
        self.maxDx = self.dx
        while w/self.maxDx>1:
            self.maxDx *= self.planeTransition

    def getNewMin(self, minVal, dx):
        if minVal<0:
            return int(minVal/dx-1)*dx
        else:
            return int(minVal/dx)*dx

    def draw(self):

        glLineWidth(1)

        dx = self.minDx
        opacity = 0.2
        while dx<self.maxDx:
            newminX = self.getNewMin(self.minX, dx)
            newminY = self.getNewMin(self.minY, dx)

            glBegin(GL_LINES)
            glColor4f(0,0.8,0.8,opacity)
            x = newminX
            while x < self.maxX:
                glVertex2f(x,self.minY)
                glVertex2f(x,self.maxY)
                x += dx
            
            y = newminY
            while y < self.maxY:
                glVertex2f(self.minX,y)
                glVertex2f(self.maxX,y)
                y += dx
            glEnd()

            dx *= self.planeTransition
            opacity += 0.2

        glBegin(GL_LINES)
        glColor4f(0,0,0.8,1)
        if self.minX*self.maxX<0:
            glVertex2f(0,self.minY)
            glVertex2f(0,self.maxY)
        if self.minY*self.maxY<0:
            glVertex2f(self.minX,0)
            glVertex2f(self.maxX,0)
        glEnd()