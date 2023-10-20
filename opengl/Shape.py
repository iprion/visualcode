from math import *
import numpy as np
from OpenGL.GL import *
from sys import *
from opengl.Constants import *

class Shape:
    def __init__(self, dashed=False):
        self.center = np.array([0,0])
        self.subShapes = []
        self.parent = None
        self.strokeColor = [1,0,0,1]
        self.fillColor = [187/255,187/255,187/255,1]
        self.strokeWidth = 1
        self.dashed = dashed   
    
    def minX(self):
        return self.getMinX() + self.center[0]
    def maxX(self):
        return self.getMaxX() + self.center[0]
    def minY(self):
        return self.getMinY() + self.center[1]
    def maxY(self):
        return self.getMaxY() + self.center[1]
    
    def getMinX(self):
        x = float_info.max
        for s in self.subShapes:
            x = min(x, s.minX())
        return x
    
    def getMaxX(self):
        x = -float_info.max
        for s in self.subShapes:
            x = max(x, s.maxX())
        return x
    
    def getMinY(self):
        x = float_info.max
        for s in self.subShapes:
            x = min(x, s.minY())

        return x

    def getMaxY(self):
        x = -float_info.max
        i=1
        for s in self.subShapes:
            x = max(x, s.maxY())
            i+=1
        return x

    def bottom(self):
        return np.array([self.center[0], self.minY()])
    
    def top(self):
        return np.array([self.center[0], self.maxY()])
    
    def left(self):
        return np.array([self.minX(), self.center[1]])
    
    def right(self):
        return np.array([self.maxX(), self.center[1]])
    
    def width(self):
        return self.getMaxX() - self.getMinX() 
    
    def height(self):
        return self.getMaxY() - self.getMinY() 

    def getCenter(self):
        return self.center
           
    def boundingBox(self):
        from opengl.BoundingBox import BoundingBox

        minx = self.minX()
        miny = self.minY()
        maxx = self.maxX()
        maxy = self.maxY()

        w = maxx-minx
        h = maxy-miny
        cx = (maxx+minx)/2
        cy = (maxy+miny)/2
        return BoundingBox(w, h, np.array([cx, cy]))
    
    def shiftBy(self, v):
        self.center = self.center + v
        return self

    def moveTo(self, p):
        self.center = p
        return self

    def moveRelativeTo(self, object, relation=TO_THE_CENTER):
        if relation==TO_THE_CENTER: 
            return self.moveTo(object.getCenter())
        elif relation==BELOW: 
            return self.moveTo(object.bottom()+self.height()/2*DOWN)
        elif relation==ABOVE: 
            return self.moveTo(object.top()+self.height()/2*UP)
        elif relation==TO_THE_LEFT: 
            return self.moveTo(object.left()).shiftBy(self.width()/2*LEFT)
        elif relation==TO_THE_RIGHT: 
            return self.moveTo(object.right()).shiftBy(self.width()/2*RIGHT)
        else:
            return self
    
    def drawLocalFrame(self):
        pass

    def drawChildrenBoundingBox(self):
        pass

    def drawChildrenPlacementBoundingBox(self):
        pass

    def add(self, subShape):
        self.subShapes.append(subShape)
        subShape.parent = self

    def remove(self, subShape):
        if subShape in self.subShapes:
            self.subShapes.remove(subShape)

    def drawGeometry(self, wireFrame):
        pass

    def draw(self):
        glPushMatrix()
        glTranslate(self.center[0],self.center[1],0)
        glPushAttrib(GL_LINE_BIT)
        glPushAttrib(GL_CURRENT_BIT)
        self.drawGeometry(False)
        self.drawGeometry(True)
        glPopAttrib(GL_CURRENT_BIT)
        glPopAttrib(GL_LINE_BIT)

        for s in self.subShapes:
            s.draw()
        glPopMatrix()

