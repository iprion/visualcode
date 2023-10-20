from opengl.Shape import *

from core.CodeNode import CodeNode
from geometries.ScenarioGeometry import ScenarioGeometry
from opengl.Shape import *

class Scenario(CodeNode):
    def __init__(self,name, parent, fields):
        super().__init__(name,parent, fields)
    
    def createGeometry(self):
        return ScenarioGeometry(self.name)