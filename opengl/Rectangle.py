from opengl.Shape import *


class Rectangle(Shape):
    def __init__(self, width, height, dashed=False):
        super().__init__(dashed)
        self.rectWidth = width
        self.rectHeight = height

    def getMinX(self):
        return -self.rectWidth/2
    def getMaxX(self):
        return self.rectWidth/2
    def getMinY(self):
        return -self.rectHeight/2
    def getMaxY(self):
        return self.rectHeight/2
    
    def setWidth(self, w):
        self.rectWidth = w

    def setHeight(self, h):
        self.rectHeight = h

    def drawGeometry(self, wireframe):

        if wireframe:
            if self.strokeWidth!=0 and self.strokeColor[3]!=0:
                w2 = self.rectWidth/2
                h2 = self.rectHeight/2
                glLineWidth(self.strokeWidth)
                glColor4fv(self.strokeColor)
                glBegin(GL_LINE_LOOP)
                glVertex2f(w2,h2)
                glVertex2f(w2,-h2)
                glVertex2f(-w2,-h2)
                glVertex2f(-w2,h2)
                glEnd()
        elif self.fillColor[3]!=0:
            w2 = self.rectWidth/2
            h2 = self.rectHeight/2
            glColor4fv(self.fillColor)
            glBegin(GL_QUADS)
            glVertex2f(w2,h2)
            glVertex2f(w2,-h2)
            glVertex2f(-w2,-h2)
            glVertex2f(-w2,h2)
            glEnd()

