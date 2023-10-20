from core.CodeNode import CodeNode
from geometries.ClassDefinitionGeometry import ClassDefinitionGeometry
from opengl.Shape import *

class ClassDefinition(CodeNode):
    def __init__(self,name,parent, fields):
        super().__init__(name,parent, fields)
    
    def createGeometry(self):
        return ClassDefinitionGeometry(self.name)

    def setInitialsubNodesRelativePositions(self):
        prev = self.subNodes[0]
        prev.geometry.moveTo([0,0])

        for x in self.subNodes[1:]:
            x.geometry.moveRelativeTo(prev.geometry,TO_THE_RIGHT).shiftBy(2*RIGHT) 
            prev = x
    
