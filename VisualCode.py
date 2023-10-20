#install dvisvgm => https://ports.macports.org/port/dvisvgm/
# => manim VisualCode.py VisualCode --renderer=opengl

import numpy as np
from core.Connexion import *
from loaders.YamlLoader import *
from loaders.PythonLoader import *
from opengl.Scene import *
import sys
from shutil import *
from execution.ScenarioExecution import ScenarioExecution

class Package():
    pass

class FileSystem:
    pass

class Directory:
    pass

class File:
    pass

class VisualCode(Scene):

    GL_SCENE_LIST = 1

    def __init__(self, args, width, height):
        super().__init__(args, width, height)    
        self.clear()
        #self.loader = YamlLoader()
        self.loader = PythonLoader()
        self.showConstraints = False
        self.showConnexionPoints = False
        self.currentScenario = None

    def clear(self):
        self.selectedComponent = None
        self.selectedArrow = None
        self.rootModule = None
        self.connexions = []

    def load(self):

        self.clear()

        self.loader.load(self.args[0], self.args[1])
        self.rootModule = self.loader.generate()
        self.rootModule.build()

        try:
            fileName = self.args[1]
            path = self.args[0]
            fullPath = path + "/" + fileName + ".yml"
            rootNodeLayoutConf = None
            fullPath = path + "/layout_" + fileName + ".yml"
            with open(fullPath, 'r') as file:                      
                docs = yaml.safe_load_all(file) 
                for doc in docs:                
                    rootNodeLayoutConf = doc
            print("File "+fullPath+" loaded")                                   
        except:
            print("Layout " + fullPath + " not found")

        self.rootModule.loadLayout(rootNodeLayoutConf)

        if self.rootModule != None:
            self.rootModule.createConnexions(self)
            for c in self.connexions:
                c.centerConnexion(True)
                c.centerConnexion(False)

        try:
            fileName = self.args[1]
            path = self.args[0]
            fullPath = path + "/" + fileName + ".yml"
            connexionsLayout = None
            fullPath = path + "/connexions_layout_" + fileName + ".yml"
            with open(fullPath, 'r') as file:                      
                docs = yaml.safe_load_all(file) 
                for doc in docs:                
                    connexionsLayout = doc
            print("File "+fullPath+" loaded")                                   
        except:
            print("Connexions layout " + fullPath + " not found")

        self.loadConnexionsLayout(connexionsLayout)
        self.rootModule.fixSubNodes(0)
        self.updateGLSceneList()

    def findConnexion(self, id):
        for c in self.connexions:
            if c.id() == id:
                return c
        return None
    
    def loadConnexionsLayout(self, layout): 

        if layout == None:
            return 
        
        for l in layout:                    
            c = self.findConnexion(l["id"])
            if c!=None:                
                print("Connexion layout found " + c.id())
                c.loadLayout(l)
               
    def dumpLayout(self): 
        layout = self.rootModule.dumpLayout()
        fullPath = self.loader.path + "/layout_" + self.loader.fileName + ".yml" 
        try:
            copy2(fullPath, fullPath+".save") 
        except:
            print("no previous layout to save")
        
        with open(fullPath, 'w') as file:
            yaml.safe_dump(layout, file,  sort_keys=False)  

        connexionsLayout = self.dumpConnexionsLayout()
        fullPath = self.loader.path + "/connexions_layout_" + self.loader.fileName + ".yml"  
        try:
            copy2(fullPath, fullPath+".save") 
        except:
            print("no previous layout to save")

        with open(fullPath, 'w') as file:
            yaml.safe_dump(connexionsLayout, file,  sort_keys=False)  
                                     
    def dumpConnexionsLayout(self):
        layout = []
        for c in self.connexions:
            layout.append(c.dumpLayout())
        return layout

    def getSelectedConnexionEnd(self):
        if self.selectedArrow.attachementStart.node == self.selectedComponent or self.selectedArrow.attachementStart.node == self.selectedComponent.parentNode or self.selectedArrow.attachementStart.node in self.selectedComponent.subNodes :
            return self.selectedArrow.attachementStart.node
        else:
            return self.selectedArrow.attachementEnd.node
        
    def keyPress(self, unicode, shift, ctrl):

        if unicode == "l":          
           self.load()           
        elif unicode=="s":
            self.dumpLayout()
        elif unicode == LEFT_ARROW: #LEFT
            if self.selectedArrow!=None:
                self.getSelectedConnexionEnd().moveArrow(self.selectedArrow, "LEFT")
        elif unicode == UP_ARROW: #UP
            if self.selectedArrow!=None:
                self.getSelectedConnexionEnd().moveArrow(self.selectedArrow, "TOP")
        elif unicode == RIGHT_ARROW: #RIGHT
            if self.selectedArrow!=None:
                self.getSelectedConnexionEnd().moveArrow(self.selectedArrow, "RIGHT")
        elif unicode == DOWN_ARROW: #DOWN
            if self.selectedArrow!=None:
                self.getSelectedConnexionEnd().moveArrow(self.selectedArrow, "BOTTOM")
        elif unicode == "+":
            if self.selectedComponent!=None:
                self.selectedArrow = self.selectedComponent.cycleArrows(self.selectedArrow, False)
        elif unicode == "-":
            if self.selectedComponent!=None:
                self.selectedArrow = self.selectedComponent.cycleArrows(self.selectedArrow, True)        
        elif unicode == "v": #-
            if self.selectedComponent!=None and self.selectedArrow!=None:
                self.selectedComponent.moveToVerticalArrow(self.selectedArrow)        
        elif unicode == "h": #-
            if self.selectedComponent!=None and self.selectedArrow!=None:
                self.selectedComponent.moveToHorizontalArrow(self.selectedArrow)
        elif unicode == "n": #-
            if self.selectedComponent!=None and self.selectedArrow!=None:
                self.selectedArrow.removeConstraint()
        elif unicode == "C":    
            self.centerAllPossibleConnexions()
        elif unicode == "x":    
            if self.selectedComponent!=None and self.selectedComponent.parentNode!=None:
                self.selectedComponent.parentNode.alignSubNodesVertically(self.selectedComponent)
        elif unicode == "y":    
            if self.selectedComponent!=None and self.selectedComponent.parentNode!=None:
                self.selectedComponent.parentNode.alignSubNodesHoritontally(self.selectedComponent)
        elif unicode == "c":
            if self.selectedComponent!=None and self.selectedArrow!=None:
                if self.selectedArrow in self.selectedComponent.incomingArrows:
                    start = False
                else:
                    start = True
                self.selectedArrow.centerConnexion(start)
        elif unicode == "1": #-
            if self.selectedArrow!=None:
                self.selectedArrow.changeNbSegments(1)        
        elif unicode == "2": #-
            if self.selectedArrow!=None:
                self.selectedArrow.changeNbSegments(2)                                            
        elif unicode == "3": #-
            if self.selectedArrow!=None:
                self.selectedArrow.changeNbSegments(3)                                            
        elif unicode == "a": #-
            self.alignAlmostAlignedConnexions()  
        elif unicode == "z": #-
            self.showConstraints = not self.showConstraints
        elif unicode == "p": #-
            self.showConnexionPoints = not self.showConnexionPoints
        
        self.updateGLSceneList()

    def alignAlmostAlignedConnexions(self):
        for c in self.connexions:
            if c.getNbSegments()==1:
                v = c.attachementStart.connexionPoint()-c.attachementEnd.connexionPoint()
                c.attachementEnd.node.shift(np.array([v[0],0]), True)
                c.attachementEnd.node.shift(np.array([0,v[1]]), True)
        if self.rootModule!=None:
            self.rootModule.updateArrows()

    
    def findConnexions(self, node, connexionSide):
        matchingConnexions = []
        for c in self.connexions:
            if c.attachementStart.node == node and c.attachementStart.connexionSide == connexionSide or c.attachementEnd.node == node and c.attachementEnd.connexionSide == connexionSide:
                matchingConnexions.append(c)
        return matchingConnexions

    def centerAllPossibleConnexions(self):
        for c in self.connexions:
            matchingConnexions = self.findConnexions(c.attachementStart.node, c.attachementStart.connexionSide)
            if len(matchingConnexions) == 1:
                c.centerConnexion(True)
            matchingConnexions = self.findConnexions(c.attachementEnd.node, c.attachementEnd.connexionSide)
            if len(matchingConnexions) == 1:
                c.centerConnexion(False)


    def createConnexion(self, begin, connexion1, end, connexion2, constraint="NONE"):
        c = Connexion(begin, connexion1, end, connexion2) 
        c.constraint = constraint  
        self.connexions.append(c)
        
    """def on_mouse_motion(self, point, dpoint):  
        if CTRL_VALUE in self.renderer.pressed_keys and self.selectedArrow!=None:
            shift = dpoint
            shift[0] *= self.camera.get_width() / 2
            shift[1] *= self.camera.get_height() / 2
            transform = self.camera.inverse_rotation_matrix
            shift = np.dot(np.transpose(transform), shift)            
            self.selectedArrow.updateUDepth(shift[1])"""


    def mouseDrag(self, screenP, worldP, deltaScreen, deltaWorld, shift, ctrl, alt):
        if self.selectedComponent!=None:
            if shift:
                deltaWorld[0] = 0
            elif ctrl:
                deltaWorld[1] = 0
            if np.linalg.norm(deltaWorld)>1e-8:
                if self.rootModule!=None:
                    self.rootModule.fixSubNodes(0)    
                self.selectedComponent.shift(np.array(deltaWorld))   
                if self.rootModule!=None:
                    self.rootModule.updateArrows()
        self.updateGLSceneList()


    def mouseDragEnd(self, screenP, worldP):
        self.updateGLSceneList()
        pass

    def mouseRelease(self, screenP, worldP):
        pass

    def mousePress(self, screenP, worldP):

        prevSelectedComp = self.selectedComponent

        newSelectedComp = None
        if self.rootModule!=None:
            newSelectedComp = self.rootModule.getSelected(worldP)
        
        if newSelectedComp != prevSelectedComp:
            if prevSelectedComp!=None:
                prevSelectedComp.deselect()
            if newSelectedComp != None:
                newSelectedComp.setSelected(0)
            self.selectedComponent = newSelectedComp

        if self.selectedArrow!=None:
            if self.selectedComponent==None:
                self.selectedArrow.unselect()            
                self.selectedArrow = None
            elif self.selectedComponent!=prevSelectedComp:
                if self.selectedArrow not in self.selectedComponent.incomingArrows and self.selectedArrow not in self.selectedComponent.outgoingArrows:
                    self.selectedArrow.unselect()            
                    self.selectedArrow = None

        if self.selectedComponent!=None and self.selectedComponent!=prevSelectedComp:
            c = self.selectedComponent.geometry.getCenter()
            print(self.selectedComponent.name + " [" + str(c[0]) + ", " +str(c[1]) +"]")        
            if (self.selectedComponent.name == "ROOT.Node1.Startup.Main.start" or self.selectedComponent.name == "ROOT.Startup.toto") and self.currentScenario==None:
                self.currentScenario = ScenarioExecution(self.selectedComponent)
   
        self.updateGLSceneList()

    def animate(self):
        if self.currentScenario!=None:
            self.currentScenario.next()

    def updateGLSceneList(self):
        glNewList(self.GL_SCENE_LIST, GL_COMPILE)
        if self.rootModule!=None:
            self.rootModule.draw()
        for c in self.connexions:
            c.draw(self.showConstraints, self.showConnexionPoints)
        glEndList()

    def draw(self):
        glCallList(self.GL_SCENE_LIST)

        if self.currentScenario!=None:
            self.currentScenario.draw()

def main():    
   args = sys.argv[1:]
   s = VisualCode(args, 1920, 1080)
   s.loop()

if __name__ == "__main__":
    main()