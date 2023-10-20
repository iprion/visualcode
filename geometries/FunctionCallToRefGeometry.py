from opengl.Rectangle import *
from opengl.RoundedRectangle import *
from opengl.Line import *

from opengl.Text import *
from core.NodeGeometry import NodeGeometry

class FunctionCallToRefGeometry(NodeGeometry):
    def __init__(self, name):        
        splitName = name.split(".")   
        self.funcName = splitName.pop()
        super().__init__(".".join(splitName))
    
    def createGeometry(self):
        self.refName = Text(self.name,1)
        self.refNameSquare =  Rectangle(self.refName.width()+0.5,self.refName.height()+0.5)

        self.functionName = Text(self.funcName,1)
        self.functionRect = Rectangle(self.functionName.width()+2,self.functionName.height()+2)
        self.functionRect.strokeColor = [0,0,0,1]
        self.functionRect.strokeWidth = 2
        self.functionRect.fillColor = [1, 1, 1,1]

        rectWidth = max(self.functionRect.width(), self.refNameSquare.width())+2
        rectHeight = self.functionRect.height()+self.refNameSquare.height()+2
        
        self.square = RoundedRectangle(rectWidth, rectHeight, 0.4, True)
        self.square.strokeColor = [0,0,0,1]
        self.square.strokeWidth = 2
        self.square.fillColor = [1, 1, 1,1]

        self.line = Line([-rectWidth/2,0],[rectWidth/2,0], True)
        self.line.strokeColor = [0,0,0,1]
        self.line.strokeWidth = 2

        self.refNameSquare.moveRelativeTo(self.square, ABOVE).shiftBy(self.refNameSquare.height()*DOWN)
        self.refName.moveRelativeTo(self.refNameSquare)        
        self.line.moveRelativeTo(self.refNameSquare,BELOW)

        self.functionRect.moveRelativeTo(self.refNameSquare, BELOW).shiftBy(DOWN)
        self.functionName.moveRelativeTo(self.functionRect)
        
        self.add(self.square)
        self.add(self.line)   
        self.add(self.refName)
        self.add(self.functionRect)   
        self.add(self.functionName)

   
    def getConnexionRectangle(self):        
        p1 = np.array([self.functionRect.minX(), self.functionRect.maxY()])
        p2 = np.array([self.functionRect.maxX(), self.functionRect.maxY()])
        p3 = np.array([self.functionRect.maxX(), self.functionRect.minY()])
        p4 = np.array([self.functionRect.minX(), self.functionRect.minY()])
        return [p1,p2,p3,p4]


    def setSelected(self,indirectlyByConstraints=-1):                 
        self.square.strokeColor = self.getConstraintDepthColor(indirectlyByConstraints)   
        self.line.strokeColor = self.getConstraintDepthColor(indirectlyByConstraints)                      

    def setBackGroundColor(self, color): 
        self.square.fillColor = color
        #self.nodeNameSquare.fillColor = color

