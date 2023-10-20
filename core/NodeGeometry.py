from opengl.Shape import *

class NodeGeometry(Shape):

    
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.createGeometry()

    def getConstraintDepthColor(self, depth):
        if depth < 0:
            return [0,0,0,1]
    
        constraintDepthColors = [[1, 0.65, 0,1], [1,0,0,1], [0,1,0,1], [0,0,1,1], [1,1,0,1], [1,0,1,1], [0,1,1,1]]
        d = min(depth, len(constraintDepthColors)-1)
        return constraintDepthColors[d]
    
    def createGeometry(self):
        pass

    def setSelected(self, indirectlyByConstraints=-1):        
        pass
    
    def getSubNodesPlacementBoundingBox(self):
        return None
    
    def getConnexionRectangle(self):                
        p1 = np.array([self.minX(), self.maxY()])
        p2 = np.array([self.maxX(), self.maxY()])
        p3 = np.array([self.maxX(), self.minY()])
        p4 = np.array([self.minX(), self.minY()])
        return [p1,p2,p3,p4]
    
    def setBackGroundColor(self, color):    
        pass   
       
    def resizeFromSubNodesBoundingBox(self, bb, updateCenter):
        return False
    
    def drawLocalFrame(self):
        w2 = self.width()/(2 * 1.05)
        h2 = self.height()/(2 * 1.05)
        glColor4f(1,0,0,1)
        glBegin(GL_LINES)
        glVertex2f(-w2, 0)
        glVertex2f(w2, 0)
        glVertex2f(0,-h2)
        glVertex2f(0,h2)
        glEnd()

    def drawChildrenPlacementBoundingBox(self):
        bb = self.getSubNodesPlacementBoundingBox()
        if bb!=None:
            bb.strokeColor = [0,0,1,1]
            bb.fillColor = [0,0,0,0]
            glPushMatrix()
            glPushAttrib(GL_LINE_BIT)
            glPushAttrib(GL_CURRENT_BIT)
            glTranslate(bb.center[0], bb.center[1],0)
            bb.drawGeometry(True)
            glPopAttrib(GL_CURRENT_BIT)
            glPopAttrib(GL_LINE_BIT)
            glPopMatrix()



        
