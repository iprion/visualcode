from opengl.Arrow import *

class NodeConnexionAttachement():
    def __init__(self, node, connexionSide):
        self.node = node
        self.rectangle = node.geometry.getConnexionRectangle()
        self.nConnexion = 1
        self.connexionSide = connexionSide
        self.node = node

    def centerConnexion(self):
        self.nConnexion = int(self.node.maxConnexionPoints()/2)+1

    def update(self, connexionSide, nConnexion):
        self.nConnexion = nConnexion
        self.connexionSide = connexionSide

    def cycleAttachements(self, connexionSide):
        if connexionSide == self.connexionSide:
            self.nConnexion = int(self.nConnexion+0.5)%self.node.maxConnexionPoints()+1
        else:
            self.centerConnexion()
            self.connexionSide = connexionSide 
    
    def dumpLayout(self):
        layout = {}
        layout["node"] = self.node.name
        layout["connexionSide"] = self.connexionSide
        layout["nConnexion"] = self.nConnexion

        return layout

    def getConnexionRectangle(self):
        rect= self.node.geometry.getConnexionRectangle()
        worldRect = []
        for p in rect:
            worldRect.append(self.node.local2world(p+self.node.geometry.getCenter()))
        return worldRect

    def connexionPoint(self, n=-1):                   
        self.rectangle = self.node.geometry.getConnexionRectangle()
        match self.connexionSide:
            case "LEFT": 
                p1 = self.rectangle[0]
                p2 = self.rectangle[3]
            case "RIGHT": 
                p1 = self.rectangle[1]
                p2 = self.rectangle[2]
            case "TOP": 
                p1 = self.rectangle[0]
                p2 = self.rectangle[1]
            case "BOTTOM": 
                p1 = self.rectangle[2]
                p2 = self.rectangle[3]
            case _ : 
                p1 = 0
                p2 = 0
        v = (p2-p1) / (self.node.maxConnexionPoints() + 1)
        if n==-1:
            p = p1 + v * self.nConnexion
        else:
            p = p1 + v * n

        return self.node.local2world(p+self.node.geometry.getCenter())
    
    def slideAttachementPoint(self, delta):
        maxConnexionPoints = self.node.maxConnexionPoints()
        if maxConnexionPoints == 1:
            return delta
        
        p1 = self.connexionPoint(1)
        p2 = self.connexionPoint(maxConnexionPoints)
        space = np.linalg.norm(p2-p1)/(maxConnexionPoints+1)
        requestedConnexionPoint = self.nConnexion + delta/space
        if requestedConnexionPoint > maxConnexionPoints:
            remainingDelta = (requestedConnexionPoint-maxConnexionPoints)*space
        elif requestedConnexionPoint < 1:
            remainingDelta = (requestedConnexionPoint-1)*space
        else:
            remainingDelta = 0
        self.nConnexion = max(1,min(maxConnexionPoints, requestedConnexionPoint))
        return remainingDelta


BOTTOM = 0
TOP = 1
LEFT = 2
RIGHT = 3
NONE = 0
VERTICAL = 1
HORIZONTAL = 2

class Connexion(Shape):
    def __init__(self, moduleStart, connexionStartSide, moduleEnd, connexionEndSide):
        super().__init__()   

        self.attachementStart = NodeConnexionAttachement(moduleStart, connexionStartSide)       
        self.attachementEnd = NodeConnexionAttachement(moduleEnd, connexionEndSide)

        p1 = self.attachementStart.connexionPoint()
        p2 = self.attachementEnd.connexionPoint()
    
        self.initialColor = moduleStart.backgroundColor.copy()
        self.initialColor[0] /= 1.5
        self.initialColor[1] /= 1.5
        self.initialColor[2] /= 1.5
        self.initialColor[3] = 1

        self.arrow = Arrow(p1,p2)
        self.arrow.strokeColor = self.initialColor
        self.arrow.strokeWidth = 1
        self.arrow.tipLength = 20
        self.add(self.arrow) 
       
        self.constraint = "NONE"

        moduleStart.addOutgoingArrow(self)
        moduleEnd.addIncomingArrow(self)
        self.updateMiddlePoints()
    
    def id(self):        
        return self.attachementStart.node.getFullName() + "_" + self.attachementEnd.node.getFullName()

    def setConstraint(self, constraint): 
            self.constraint = constraint

    def dumpLayout(self):
        layout = {}
        layout["id"] = self.id()   
        layout["nbSegments"] = self.arrow.nbSegments
        layout["start"] = self.attachementStart.dumpLayout()   
        layout["end"] = self.attachementEnd.dumpLayout()       
        layout["constraint"] = self.constraint     
        return layout
    
    def loadLayout(self,layout):
        lstart = layout["start"]
        lend = layout["end"]
        self.updateStartAttachement(lstart["connexionSide"], lstart["nConnexion"])
        self.updateEndAttachement(lend["connexionSide"], lend["nConnexion"])
        self.changeNbSegments(layout["nbSegments"])
        self.updateConstraints(layout["constraint"])

    def centerConnexion(self, start):
        if start:
            self.attachementStart.centerConnexion()   
            self.arrow.setStart(self.attachementStart.connexionPoint())
        else:
            self.attachementEnd.centerConnexion()   
            self.arrow.setEnd(self.attachementEnd.connexionPoint())
        self.updateMiddlePoints()

    def updateUDepth(self,delta):
        self.arrow.updateUDepth(delta)

    def getNbSegments(self):
        return self.arrow.nbSegments

    def changeNbSegments(self, nbSegments):
        if nbSegments == self.arrow.nbSegments:
            return
        self.arrow.nbSegments = nbSegments
        self.updateMiddlePoints()

    def updateMiddlePoints(self):
        if self.arrow.nbSegments == 2 :
            self.updateMiddle1()                
        elif self.arrow.nbSegments == 3 :
            self.updateMiddle2() 

    def updateStartAttachement(self, connexionSide, nConnexion):
        self.attachementStart.update(connexionSide, nConnexion)    
        self.arrow.setStart(self.attachementStart.connexionPoint())
        self.updateMiddlePoints()

    def updateEndAttachement(self, connexionSide, nConnexion):
        self.attachementEnd.update(connexionSide, nConnexion)  
        self.arrow.setEnd(self.attachementEnd.connexionPoint())
        self.updateMiddlePoints()

    def cycleStartAttachements(self, connexionSide):
        self.attachementStart.cycleAttachements(connexionSide)    
        self.arrow.setStart(self.attachementStart.connexionPoint())
        self.updateMiddlePoints()

    def cycleEndAttachements(self, connexionSide):
        self.attachementEnd.cycleAttachements(connexionSide)  
        self.arrow.setEnd(self.attachementEnd.connexionPoint())
        self.updateMiddlePoints()

    def updateStart(self):
        self.arrow.setStart(self.attachementStart.connexionPoint())
        self.updateMiddlePoints()
    
    def updateEnd(self):    
        self.arrow.setEnd(self.attachementEnd.connexionPoint())
        self.updateMiddlePoints()

    def updateConstraints(self, constraint):
        self.constraint = constraint

    def updateMiddle2(self):

        p1 = self.attachementStart.connexionPoint()
        p2 = self.attachementEnd.connexionPoint()

        if self.attachementStart.connexionSide=='TOP':              
            midPoint1 = [p1[0],max(p1[1], p2[1])+self.arrow.uDepth]
            midPoint2 = [p2[0], midPoint1[1]]
        elif self.attachementStart.connexionSide=='BOTTOM':              
            midPoint1 = [p1[0],max(p1[1], p2[1])-self.arrow.uDepth]
            midPoint2 = [p2[0],midPoint1[1]]
        elif self.attachementStart.connexionSide=='LEFT':
            midPoint1 = [max(p1[0], p2[0])-self.arrow.uDepth,p1[1]]
            midPoint2 = [midPoint1[0],p2[1]]
        elif self.attachementStart.connexionSide=='RIGHT':
            midPoint1 = [max(p1[0], p2[0])+self.arrow.uDepth,p1[1]]
            midPoint2 = [midPoint1[0],p2[1]]

        self.arrow.updateMiddlePoints(midPoint1, midPoint2)

    def updateMiddle1(self): 

        p1 = self.attachementStart.connexionPoint()
        p2 = self.attachementEnd.connexionPoint()

        if self.attachementStart.connexionSide=='TOP' or self.attachementStart.connexionSide=='BOTTOM':               
            midPoint = np.array([p1[0],p2[1]])
        elif self.attachementStart.connexionSide=='LEFT' or self.attachementStart.connexionSide=='RIGHT':
            midPoint = np.array([p2[0],p1[1]])

        self.arrow.updateMiddlePoint(midPoint)


    def select(self):
        self.arrow.strokeColor = [0,0,0,1]

    def unselect(self):
        self.arrow.strokeColor = self.initialColor

    def drawConnexionsPoints(self, attachement):
        n = attachement.node.maxConnexionPoints()    
        glPointSize(5)
        glColor4f(1,0,0,1)
        glBegin(GL_POINTS)
        for i in range(n):
            p = attachement.connexionPoint(i+1)
            glVertex2fv(p)
        glEnd()
    

    def removeConstraint(self):
        self.constraint = "NONE"

    def draw(self, showConstraints, showConnexionPoints):
        
        savedColor = self.arrow.strokeColor.copy()
        
        if self.constraint != "NONE" and showConstraints:
            if self.attachementStart.node.constraintSelectionDepth>=0:
                self.arrow.strokeColor = self.attachementStart.node.geometry.getConstraintDepthColor(self.attachementStart.node.constraintSelectionDepth)
        
        super().draw()

        self.arrow.strokeColor = savedColor
        
        if showConnexionPoints:
            self.drawConnexionsPoints(self.attachementStart)
            self.drawConnexionsPoints(self.attachementEnd)
        