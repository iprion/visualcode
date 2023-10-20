
from core.NodeGeometry import *
from opengl.Rectangle import *
from opengl.Text import *

class SimpleFunctionDefinitionGeometry(NodeGeometry):
    def __init__(self, name):
        super().__init__(name)
              
    def createGeometry(self):
        self.text = Text(self.name,1)        
        self.square = Rectangle(self.text.width()+0.5,self.text.height()+2)       
        self.square.strokeColor = [0,0,0,1]
        self.square.strokeWidth = 2
        self.square.fillColor = [1, 1, 1,1]   
        self.text.moveRelativeTo(self.square)
        self.add(self.square)
        self.add(self.text) 

    def setSelected(self,indirectlyByConstraints=-1):        
        self.square.strokeColor = self.getConstraintDepthColor(indirectlyByConstraints)           

     
    def getConnexionRectangle(self):                        
        p1 = np.array([self.square.minX(), self.square.maxY()])
        p2 = np.array([self.square.maxX(), self.square.maxY()])
        p3 = np.array([self.square.maxX(), self.square.minY()])
        p4 = np.array([self.square.minX(), self.square.minY()])
        return [p1,p2,p3,p4]