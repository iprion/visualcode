from opengl.Shape import *

class Polygon(Shape):
    def __init__(self, points, dashed=False):
        super().__init__(dashed)
        self.points = points
    

    def getMinX(self):
        x = self.points[0][0]
        for p in self.points:
            x = min(x, p[0])
        return x
    def getMaxX(self):
        x = self.points[0][0]
        for p in self.points:
            x = max(x, p[0])
        return x    
    def getMinY(self):
        x = self.points[0][1]
        for p in self.points:
            x = min(x, p[1])
        return x
    def getMaxY(self):
        x = self.points[0][1]
        for p in self.points:
            x = max(x, p[1])
        return x
    
    def setPoints(self, points):
        self.points.clear()
        for p in self.points:
            self.points.append(p)
    
    def drawGeometry(self, wireFrame):

        if wireFrame:
            if self.strokeWidth!=0 and self.strokeColor[3]!=0:
                glLineWidth(self.strokeWidth)
                glColor4fv(self.strokeColor)
                glBegin(GL_LINE_LOOP)
                for p in self.points:
                    glVertex2fv(p)
                glEnd()
        elif self.fillColor[3]!=0:
            glColor4fv(self.fillColor)
            glBegin(GL_POLYGON)
            for p in self.points:
                glVertex2fv(p)
            glEnd()
        
  