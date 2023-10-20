from opengl.Shape import *
from definitions.ClassDefinition import ClassDefinition
from definitions.Scenario import Scenario


class RootDefinition(ClassDefinition):
    def __init__(self,name,parent, fields):
        super().__init__("Root",parent, fields)
