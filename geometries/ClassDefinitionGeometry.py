from core.NodeGeometry import NodeGeometry
from opengl.Text import *
from opengl.Rectangle import *
from opengl.BoundingBox import BoundingBox

class ClassDefinitionGeometry(NodeGeometry):
    def __init__(self,name):
        super().__init__(name)
    
    def createGeometry(self):
        self.nodeName = Text(self.name, 3)

        self.nodeNameSquare =  Rectangle(self.nodeName.width()+2,self.nodeName.height()+1)
        self.nodeNameSquare.strokeColor = [0,0,0,1]
        self.nodeNameSquare.strokeWidth = 2
        self.nodeNameSquare.fillColor = [221,221,221,1]
        
        self.square = Rectangle(1,1)
        self.square.strokeColor = [0,0,0,1]
        self.square.strokeWidth = 2
        self.square.fillColor = [221,221,221,1]

        self.add(self.square)
        self.add(self.nodeNameSquare)   
        self.add(self.nodeName)
    
    def getSubNodesPlacementBoundingBox(self):
        return BoundingBox(self.square.width(), self.square.height(), self.square.getCenter())
    
    def setBackGroundColor(self, color): 
        self.square.fillColor = color
        self.nodeNameSquare.fillColor = color

    def setSelected(self, indirectlyByConstraints=-1):        
        self.square.strokeColor = self.getConstraintDepthColor(indirectlyByConstraints)
        self.nodeNameSquare.strokeColor = self.getConstraintDepthColor(indirectlyByConstraints)                                      
      
        
    def resizeFromSubNodesBoundingBox(self, bb, updateCenter):  
        newWidth = max(bb.width()+4,self.nodeName.width()+2)
        newHeight = bb.height() + 4
        
        delta = bb.getCenter() + self.nodeNameSquare.height()*0.5*UP
        needsUpdate = fabs(newWidth-self.square.width())>1e-8 or fabs(newHeight-self.square.height())>1e-8 or np.linalg.norm(delta) > 1e-8
        if needsUpdate:
            
            if updateCenter:
                self.shiftBy(delta)
            else:
                self.square.moveTo([0,0]).shiftBy(self.nodeNameSquare.height()*0.5*DOWN)

            self.square.setWidth(newWidth)
            self.square.setHeight(newHeight)
            self.nodeNameSquare.setWidth(newWidth)
            self.nodeNameSquare.moveRelativeTo(self.square, ABOVE)
            self.nodeName.moveRelativeTo(self.nodeNameSquare)   
            return delta
        else:
            return ZERO
    
    def getConnexionRectangle(self):    
        p1 = np.array([self.square.minX(), self.nodeNameSquare.maxY()])
        p2 = np.array([self.square.maxX(), self.nodeNameSquare.maxY()])
        p3 = np.array([self.square.maxX(), self.square.minY()])
        p4 = np.array([self.square.minX(), self.square.minY()])
        return [p1,p2,p3,p4]
