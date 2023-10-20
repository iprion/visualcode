from core.CodeNode import CodeNode
from geometries.FunctionDefinitionGeometry import FunctionDefinitionGeometry
from geometries.SimpleFunctionDefinitionGeometry import SimpleFunctionDefinitionGeometry

from opengl.Shape import *

class FunctionDefinition(CodeNode):

    def __init__(self, name, parent, fields):
        super().__init__(name,parent, fields)        
    
    def createGeometry(self):
        if len(self.subNodes)==0:
            return SimpleFunctionDefinitionGeometry(self.name)
        else:
            return FunctionDefinitionGeometry(self.name)

    def setInitialsubNodesRelativePositions(self):
        prev = self.subNodes[0]
        prev.geometry.moveTo([0,0])
        for x in self.subNodes:
            x.geometry.moveRelativeTo(prev.geometry,BELOW).shiftBy(2*DOWN)
            prev = x
            
    def createConnexions(self,scene):        
        if len(self.subNodes)>0:
            scene.createConnexion(self, "BOTTOM", self.subNodes[0], "TOP", "NONE")

        prev = None
        for s in self.subNodes:                
            if prev!=None:
                scene.createConnexion(prev, "BOTTOM", s, "TOP", "VERTICAL")
            s.createConnexions(scene)
            prev = s    

    def maxConnexionPoints(self):
        return 1


