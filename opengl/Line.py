from opengl.Shape import *

class Line(Shape):
    def __init__(self, start, end, dashed=False):
        super().__init__(dashed)
        self.start = start
        self.end = end

    def getMinX(self):
        return min(self.start[0], self.end[0])
    def getMaxX(self):
        return max(self.start[0], self.end[0])
    def getMinY(self):
        return min(self.start[1], self.end[1])
    def getMaxY(self):
        return max(self.start[1], self.end[1])
    
    def updateEnds(self, start, end):
        self.start = start

    
    def drawGeometry(self, wireFrame):
        
        if wireFrame or self.strokeWidth==0 or self.strokeColor[3]==0:
            return

        glLineWidth(self.strokeWidth)
        glColor4fv(self.strokeColor)
        glBegin(GL_LINES)
        glVertex2fv(self.start)
        glVertex2fv(self.end)
        glEnd()
