from opengl.Shape import *
      
class Arrow(Shape):

    def __init__(self, start, end, dashed=False):
        super().__init__(dashed)
        self.tipLength = 10
        self.start = np.array(start)
        self.end = np.array(end)
        self.nbSegments = 1
        self.uDepth = 0.5
        self.midPoint1 = np.array([0,0])
        self.midPoint2 = np.array([0,0])

    def getMinX(self):
        return min(self.start[0], self.end[0])
    def getMaxX(self):
        return max(self.start[0], self.end[0])
    def getMinY(self):
        return min(self.start[1], self.end[1])
    def getMaxY(self):
        return max(self.start[1], self.end[1])
    
    def getPoints(self):
        points = [self.start]
        if self.nbSegments>1:
            points.append(self.midPoint1)
        if self.nbSegments>2:
            points.append(self.midPoint2)
        points.append(self.end)
        return points
    
    def updateEnds(self, start, end):
        self.start = np.array(start)
        self.end = np.array(end)
    
    def normal(self, v):
        norm = np.linalg.norm(v)
        if norm == 0: 
            return v
        return np.array([v[1],-v[0]])/ norm
                    
    def updateUDepth(self,delta):
        if self.nbSegments == 3:
            self.uDepth += delta
            self.updateMiddle2()              
    
    def updateStart(self ,delta):
        self.start += np.array(delta)      
    
    def updateEnd(self , delta):
        self.end += np.array(delta)       
    
    def updateMiddlePoint(self, p):
        self.midPoint1 = np.array(p)
    
    def updateMiddlePoints(self, p1, p2):
        self.midPoint1 = np.array(p1)
        self.midPoint2 = np.array(p2)

    def setStart(self, p):
        self.start = p

    def setEnd(self, p):
        self.end = p

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end    
       
    def drawGeometry(self, wireFrame):
        
        if wireFrame and (self.strokeWidth==0 or self.strokeColor[3]==0):
            return

        glColor4fv(self.strokeColor)
        
        if self.nbSegments == 1:
            self.drawSegment(self.start, self.end)
        elif self.nbSegments == 2:
            self.drawSegment(self.start, self.midPoint1)
            self.drawSegment(self.midPoint1, self.end)
        elif self.nbSegments == 3:
            self.drawSegment(self.start, self.midPoint1)
            self.drawSegment(self.midPoint1, self.midPoint2)
            self.drawSegment(self.midPoint2, self.end)
    
    def drawSegment(self, p1, p2):

        d = np.subtract(p2, p1)
        n = self.strokeWidth * self.normal(d)
        v1 = p1 + 0.5 * n
        v2 = v1 - n
        v3 = v2 + d
        v4 = v3 + n
        glBegin(GL_QUADS)
        glVertex2fv(v1)
        glVertex2fv(v2)
        glVertex2fv(v3)
        glVertex2fv(v4)
        glEnd()

