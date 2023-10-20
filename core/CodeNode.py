from loaders.NodeInstanceBuilder import *
from opengl.BoundingBox import *

class CodeNode():

    CURRENT_GL_LIST = 2

    def __init__(self, name, parent, fields):
        super().__init__()
        self.name = name        
        self.parentNode = parent
        self.fields = fields
        self.constraintSelectionDepth = -1
        self.subNodes = []
        self.noGeometrySubNodes = []
        self.nextSibling = None
        self.prevSibling = None
        self.incomingArrows = []
        self.outgoingArrows = []
        self.geometry = None
        self.depthInModuleHierarchy = self.getDepth()
        self.backgroundColor = [187/255.0,187/255.0,187/255.0,1]  #LIGHT_GREY
        self.attributes = {}
        self.isAncestorSelected = False
        self.isFixed = 0
        self.glList = CodeNode.CURRENT_GL_LIST
        print("GLLIST = "+str(self.glList))
        CodeNode.CURRENT_GL_LIST += 1        


    def setSelected(self, depth):
        self.constraintSelectionDepth = depth
        self.geometry.setSelected(depth)

    def hasGeometry(self):
        return True
    
    def getDepth(self):
        parent = self.parentNode        
        depth = 0
        while parent!=None:
            depth += 1
            parent = parent.parentNode
        return depth
    
    def overlap(self, node1, node2):
        bb1 = node1.geometry.boundingBox()
        bb2 = node2.geometry.boundingBox()
        return bb1.getOverlap(bb2, 2)

    def containsSelected(self):
        if self.constraintSelectionDepth==0:
            return True
        for x in self.subNodes:  
            if x.containsSelected():
                return True
        return False
    
    def selectedSubModule(self):
        for x in self.subNodes:
            if x.containsSelected():
                return x
        return None


    def build(self):      

        print("  "*self.depthInModuleHierarchy + self.name + " build STARTED")                    
            
        self.geometry = self.createGeometry()

        for s in self.subNodes:
            s.build()

        self.geometry.setBackGroundColor(self.backgroundColor)

        if len(self.subNodes)!=0:
            self.setInitialsubNodesRelativePositions()                
        self.resizeSelf(False)
        self.centerSubNodesInBoundingBox(self.geometry.getSubNodesPlacementBoundingBox())

        print("  "*self.depthInModuleHierarchy + self.name + " build DONE")                    

        self.updateGLList()


    def moveToVerticalArrow(self, selectedArrow):
        if selectedArrow in self.incomingArrows:
            delta = selectedArrow.attachementEnd.connexionPoint() - selectedArrow.attachementStart.connexionPoint()
        elif selectedArrow in self.outgoingArrows:
            delta = selectedArrow.attachementStart.connexionPoint() - selectedArrow.attachementEnd.connexionPoint()
        else:
            return
        
        delta[1] = 0
        self.shift(-delta)
        selectedArrow.setConstraint("VERTICAL")        
        self.getTopModule().updateArrows()

    def moveToHorizontalArrow(self, selectedArrow):
        if selectedArrow in self.incomingArrows:
            delta = selectedArrow.attachementEnd.connexionPoint() - selectedArrow.attachementStart.connexionPoint()
        elif selectedArrow in self.outgoingArrows:
            delta = selectedArrow.attachementStart.connexionPoint() - selectedArrow.attachementEnd.connexionPoint()
        else:
            return  
        delta[0] = 0          
        self.shift(-delta)      
        selectedArrow.setConstraint("HORIZONTAL")
        self.getTopModule().updateArrows()

    def maxConnexionPoints(self):
        nbConnexionPoints = max(10, len(self.incomingArrows) + len(self.outgoingArrows))
        if nbConnexionPoints%2 == 0:
            nbConnexionPoints+=1
        return nbConnexionPoints
       

    def moveArrow(self, selectedArrow, connexion):
        if selectedArrow == None:
            return
        if selectedArrow in self.outgoingArrows:
            selectedArrow.cycleStartAttachements(connexion)
        elif selectedArrow in self.incomingArrows:
            selectedArrow.cycleEndAttachements(connexion)
        else:
            return
    
    def getSubNodesArrows(self):
        arrows = []
        for s in self.subNodes:
            arrows += s.incomingArrows + s.outgoingArrows
        return arrows
    
    def cycleArrows(self, prevArrow, prev):               
        arrows = self.incomingArrows + self.outgoingArrows
        if len(arrows) == 0:
            arrows = self.getSubNodesArrows()
            if len(arrows) == 0:
                if self.parentNode != None:
                    arrows = self.parentNode.incomingArrows + self.parentNode.outgoingArrows

        if len(arrows)==0:
            return None
        
        arrow = None
        if prevArrow==None:
            arrow = arrows[0]
        elif prevArrow in arrows:
            if prev:            
                i = (arrows.index(prevArrow)-1)%len(arrows)
            else:
                i = (arrows.index(prevArrow)+1)%len(arrows)
            arrow = arrows[i]               

        if arrow!=prevArrow and prevArrow!=None:         
            prevArrow.unselect()

        if arrow != None:
            arrow.select()

        return arrow                             


    def createConnexions(self,scene):
       
        for a in self.attributes:
            value = self.attributes[a]
            print("Trying to find att reference for "+value)
            subM = self.findReferedModule(value)
            if subM!=None:
                print("found att reference for "+value)
                scene.createConnexion(self, 'LEFT', subM, 'TOP')

        for s in self.subNodes:
            s.createConnexions(scene)

    def setInitialsubNodesRelativePositions(self):
        pass

    def centerSubNodesInBoundingBox(self, bb):
        
        if len(self.subNodes)==0:
            return 
        
        subNodesBB = self.subNodesBoundingBox()
        delta = bb.getCenter()-subNodesBB.getCenter()
        for x in self.subNodes:
           x.geometry.shiftBy(delta)

    def addIncomingArrow(self, arrow):
        self.incomingArrows.append(arrow)
        print(self.name+" has now " + str(len(self.incomingArrows)) + " incoming arrows")
        
    def addOutgoingArrow(self, arrow):
        self.outgoingArrows.append(arrow)    
        print(self.name+" has now " + str(len(self.outgoingArrows)) + " outgoing arrows")

    def findReferedModule(self,name):        
        token = name.split(".")        
        if token[0] == self.name:
            if len(token)==1:
                return self
            for s in self.subNodes:
                if s.name == token[1]:
                    token.pop(0)                    
                    return s.findReferedModule(".".join(token))
            return None
        elif self.parentNode!=None:
            return self.parentNode.findReferedModule(name)
        else:
            return None

    def dumpLayout(self):
        modConf = {}
        modConf["center"] = self.geometry.getCenter().tolist()
        subNodesConf = []
        for s in self.subNodes:
            subNodesConf.append(s.dumpLayout())
        if len(subNodesConf)!=0:
            modConf["subNodes"] = subNodesConf
        conf = {}
        conf[self.name] = modConf
        return conf

    def getSubModule(self,name):
        for s in self.subNodes:
            if s.getName() == name:
                return s
        return None

    def isLeaf(self):
        return self.subNodes.length == 0

    def getSelected(self,point):
        bb = self.geometry.boundingBox()
        if not bb.containsPoint(point):
            return None
        p = point-self.geometry.getCenter()
        for s in self.subNodes:
            selSub = s.getSelected(p)
            if selSub!=None:
                return selSub

        return self
    
    def setAncestorSelected(self, select):
        self.isAncestorSelected = select
        for s in self.subNodes:
            s.setAncestorSelected(select)

    def deselect(self, childOnly = False):
        self.setSelected(-1)
        for s in self.subNodes:
            s.setAncestorSelected(False)


    def getTopModule(self):
        if self.parentNode!=None:
            return self.parentNode.getTopModule()
        return self

    def fixSubNodes(self, fix):
        self.isFixed = fix
        for s in self.subNodes:
            s.fixSubNodes(fix)

    def deselectConstraint(self):
        if self.constraintSelectionDepth!=0:
            self.setSelected(-1)
        for n in self.subNodes:
            n.deselectConstraint()

    def shift(self, delta):
        
        if np.linalg.norm(delta)<1e-8:     
            return True

        if self.isFixed == 10:
            print("FIX " + self.name)
            return True
                
        #print("   "*depth + self.name + " SHIFTED BY " + str(delta))
        self.isFixed += 1
        success = True
        if fabs(delta[0])>1e-8:
            self.geometry.shiftBy(np.array([delta[0],0]))            
            success = success and self.solveConstraints(True, True, True)
        if fabs(delta[1])>1e-8:
            self.geometry.shiftBy(np.array([0,delta[1]]))            
            success = success and self.solveConstraints(False, True, True)
    
        self.updateGLList()

        return True         
    
    def solveConstraints(self, verticalConstraints, solveForParent, solveForChildren):
        
        self.resizeSelf(True)

        success = True

        success = success and self.solveDirectConstraints(verticalConstraints)

        if solveForChildren:
            for n in self.subNodes:               
                success = success and n.solveConstraints(verticalConstraints, False, True)           

        if solveForParent and self.parentNode!=None:
            return success and self.parentNode.solveConstraints(verticalConstraints, True, False)                    

        return success
                    

    def solveDirectConstraints(self, verticalConstraints):            
        success = True    

        # detect and solve collisions with siblings first        
        for n in self.siblings():                                  
            if n != self:  
                v = self.overlap(self, n)
                if verticalConstraints:
                    v[1] = 0
                else:
                    v[0] = 0
                success = success and n.shift(v)

        # detect and solve connexions constraints
        for c in self.incomingArrows:
            success = success and self.solveConnexionConstraint(verticalConstraints, c.constraint, c.attachementEnd, c.attachementStart)

        for c in self.outgoingArrows:
            success = success and self.solveConnexionConstraint(verticalConstraints, c.constraint, c.attachementStart, c.attachementEnd)        

        return success 

    def solveConnexionConstraint(self, verticalConstraints, constraint, selfAttachement, otherEndAttachement):
        
        if verticalConstraints and constraint == "VERTICAL":                     
            delta = selfAttachement.connexionPoint() - otherEndAttachement.connexionPoint()
            if fabs(delta[0]) < 1e-8:     
                return True
            d = otherEndAttachement.slideAttachementPoint(delta[0])
            d = -selfAttachement.slideAttachementPoint(-d)         
            delta = np.array([d,0])
        elif not verticalConstraints and constraint == "HORIZONTAL":                            
            delta = selfAttachement.connexionPoint() - otherEndAttachement.connexionPoint()
            if fabs(delta[1]) < 1e-8:     
                return True
            d = otherEndAttachement.slideAttachementPoint(delta[1])
            d = -selfAttachement.slideAttachementPoint(-d)            
            delta = np.array([0,d])
        else:
            return True
        
        #print("   "*(depth+2) + otherNode.name + str(v))        
        return otherEndAttachement.node.shift(delta)        


    def resizeSelf(self, updateCenter, boundingBox=None):
        if len(self.subNodes)==0:
            return False

        if boundingBox==None:
            bb = self.subNodesBoundingBox()
        else:
            bb = boundingBox

        delta = self.geometry.resizeFromSubNodesBoundingBox(bb, updateCenter)   
        if delta.any():
            for s in self.subNodes:
                s.geometry.shiftBy(-1*delta)
            self.updateGLList()
            return True
        else:
            return False

    def updateArrows(self):
        
        for a in self.incomingArrows:                
            a.updateEnd()
                
        for a in self.outgoingArrows:                
            a.updateStart()    

        for s in self.subNodes:                
            s.updateArrows()

    def subNodesBoundingBox(self):
        minx = float_info.max
        miny = float_info.max
        maxx = -float_info.max
        maxy = -float_info.max
        for s in self.subNodes:
            maxx = max(maxx,s.geometry.maxX())
            maxy = max(maxy,s.geometry.maxY())
            minx = min(minx,s.geometry.minX())
            miny = min(miny,s.geometry.minY())

        w = maxx-minx
        h = maxy-miny
        cx = (maxx+minx)/2
        cy = (maxy+miny)/2
        return BoundingBox(w, h, np.array([cx, cy]))

    def siblings(self):
        if self.parentNode==None:
            return []
        else:
            return self.parentNode.subNodes

    def createGeometry(self):
        pass

    def updateGLList(self):

        #for s in self.subNodes:
        #   s.updateGLList()

        glNewList(self.glList, GL_COMPILE)
        self.geometry.draw()
        
        if len(self.subNodes)>0:
            glPushMatrix()
            glTranslate(self.geometry.center[0],self.geometry.center[1],0)

            #self.geometry.drawLocalFrame()
            for s in self.subNodes:
                s.draw()

            #self.drawChildrenBoundingBox()
            #self.geometry.drawChildrenPlacementBoundingBox()

            glPopMatrix()

        glEndList()

    def draw(self):
        glCallList(self.glList)

    def drawChildrenBoundingBox(self):
        
        if len(self.subNodes)==0:
            return 
        
        bb = self.subNodesBoundingBox()
        bb.strokeColor = [0,1,0,1]
        bb.fillColor = [0,0,0,0]
        bb.strokeWidth = 2
        glPushMatrix()
        glPushAttrib(GL_LINE_BIT)
        glPushAttrib(GL_CURRENT_BIT)
        glTranslate(bb.center[0], bb.center[1],0)
        bb.drawGeometry(True)
        glPopAttrib(GL_CURRENT_BIT)
        glPopAttrib(GL_LINE_BIT)
        glPopMatrix()

    def local2world(self, point):
        if self.parentNode == None:
            return point
        
        p = self.parentNode
        x = np.array(point)
        while p!=None:
            x = x + p.geometry.getCenter()
            p = p.parentNode
        return x

    def world2local(self, point):
        if self.parentNode == None:
            return point
        
        p = self.parentNode
        x = np.array(point)
        while p!=None:
            x = x - p.geometry.getCenter()
            p = p.parentNode
        return x

    def findClassWithName(self, names):
        for s in self.subNodes:
            if s.name == names[0]:
                p = self
                i=1
                while p!=None:
                    if i==len(names):
                        return False
                    if p.name == names[i]:
                        if i == len(names)-1:
                            return True
                        else:
                            p = p.parentNode                            
                    else:
                        p = None                                            
                    i+=1
                
        
        if self.parentNode==None or len(names)==0:
            return False
        else:
            return self.parentNode.findClassWithName(names)
        
    def loadLayout(self, layoutConf):
        
        if layoutConf==None:
            return 
        
        if self.name in layoutConf:
            nodeConf = layoutConf[self.name]            
            c = np.array(nodeConf["center"])
            self.geometry.moveTo(c) 
            print("Position found for "+self.name+" ["+str(c[0])+","+str(c[1])+"]")
            if "subNodes" in layoutConf[self.name]:
                subNodesConf = nodeConf["subNodes"]
                i=0
                for s in self.subNodes:
                    if i<len(subNodesConf):
                        s.loadLayout(subNodesConf[i])
                    i+=1
            self.resizeSelf(False)
            self.updateGLList()
        else:
            print("Position NOT found for "+self.name)
    
    def addAttribute(self, attName, attValue, attType):
        print("adding attribute "+ attName+" = "+attValue)        
        self.attributes[attName] = attValue

    def alignSubNodesVertically(self, node):
        c = node.geometry.getCenter()
        for s in self.subNodes:
            if s!=node:
                delta = c - s.geometry.getCenter()
                delta[1] = 0                
                s.shift(delta)
        return self.getTopModule().updateArrows()
    
    def alignSubNodesHoritontally(self, node):
        c = node.geometry.getCenter()
        for s in self.subNodes:
            if s!=node:
                delta = c - s.geometry.getCenter()
                delta[0] = 0                
                s.shift(delta)
        return self.getTopModule().updateArrows()

    def getFullName(self):
        p = self.parentNode
        if p==None:
            return self.name
        
        fullName = ""
        while p!=None:
            fullName = p.name + "." + fullName
            p = p.parentNode
        fullName += self.name
        return fullName                                  
