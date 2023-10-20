from core.NodeGeometry import NodeGeometry
from opengl.Rectangle import *
from opengl.Text import *
from opengl.BoundingBox import BoundingBox

class FunctionDefinitionGeometry(NodeGeometry):
    
    def __init__(self, name):
        super().__init__(name)        
    
    def createGeometry(self):
        self.square = Rectangle(1,1)
        self.square.strokeColor = [0,0,0,1]
        self.square.strokeWidth = 2

        self.functionName = Text(self.name, 2)

        self.functionNameRect = Rectangle(self.functionName.width()+1,self.functionName.height()+1)
        self.functionNameRect.strokeColor = [0,0,0,1]
        self.functionNameRect.strokeWidth = 2
        self.functionNameRect.fillColor = [1, 1, 1,1]
            
        self.add(self.square)
        self.add(self.functionNameRect)   
        self.add(self.functionName)
    
    def getSubNodesPlacementBoundingBox(self):
        c = self.square.getCenter().copy()
        h2 = self.functionNameRect.height()*0.5
        c[1] -= h2*0.5
        return BoundingBox(self.square.width(), self.square.height()-h2, c)
    
    def getConnexionRectangle(self):    
        p1 = np.array([self.functionNameRect.minX(), self.functionNameRect.maxY()])
        p2 = np.array([self.functionNameRect.maxX(), self.functionNameRect.maxY()])
        p3 = np.array([self.functionNameRect.maxX(), self.functionNameRect.minY()])
        p4 = np.array([self.functionNameRect.minX(), self.functionNameRect.minY()])
        return [p1,p2,p3,p4]
    
    def setBackGroundColor(self, color):
        self.square.fillColor = color 
        
    def setSelected(self,indirectlyByConstraints=-1):        
        self.square.strokeColor = self.getConstraintDepthColor(indirectlyByConstraints)  
        self.functionNameRect.strokeColor = self.getConstraintDepthColor(indirectlyByConstraints)      
       
    def resizeFromSubNodesBoundingBox(self, bb, updateCenter):
        newWidth = max(bb.width(),self.functionNameRect.width())+4
        newHeight = bb.height() + self.functionNameRect.height()*0.5 + 4
        needsUpdate = newWidth!=self.square.width() or newHeight!=self.square.height()
        if not needsUpdate and updateCenter and not np.array_equal(self.square.getCenter(), bb.getCenter()):
            needsUpdate = True
        needsUpdate = True
        if needsUpdate:
            delta = bb.getCenter() + self.functionNameRect.height()*0.5*UP
            if updateCenter:
                self.shiftBy(delta)
            else:            
                 self.square.moveTo([0,0]).shiftBy(self.functionNameRect.height()*0.25*DOWN)
            self.square.setWidth(newWidth)
            self.square.setHeight(newHeight)
            self.functionNameRect.moveRelativeTo(self.square, ABOVE).shiftBy(0.5*self.functionNameRect.height()*DOWN)
            self.functionName.moveRelativeTo(self.functionNameRect)
            return delta
        else:
            return np.array([0,0])        