from core.CodeNode import CodeNode
from geometries.FunctionCallToSelfGeometry import FunctionCallToSelfGeometry
from geometries.FunctionCallToRefGeometry import FunctionCallToRefGeometry
from opengl.Shape import *

class FunctionCall(CodeNode):
    def __init__(self, name, parent, fields):
        super().__init__(name,parent, fields)
        
    def createGeometry(self):        

        print("Searching for constructor for "+self.name)
        if self.parentNode!=None:
            isCallToContructor = self.parentNode.findClassWithName(self.name.split(".")[::-1])        
            if isCallToContructor:
                print("Constructor Found "+self.name)

        if "." in self.name:
            return FunctionCallToRefGeometry(self.name)
        else:
            return FunctionCallToSelfGeometry(self.name)         


    def createConnexions(self,scene):
        if "." in self.name:
            subM = self.findReferedModule(self.name)
            if subM!=None:
                scene.createConnexion(self, 'LEFT', subM, 'TOP')
    
    def maxConnexionPoints(self):
        return 1