
from definitions.FunctionDefinition import *
from core.Connexion import *


class ScenarioExecution:
    totalsize = 0

    class ConnexionToNext:

        def __init__(self, fromNode , nextNode):
            self.nextNode = nextNode
            self.fromNode = fromNode
            self.movingPoints = []
            self.dirToNext = nextNode.p - fromNode.p
            self.distanceToNext = np.linalg.norm(self.dirToNext)
            self.dirToNext = self.dirToNext/self.distanceToNext
            self.nbInjected = 0
        
        def inject(self, d):
            self.movingPoints.insert(0, d)
            self.nbInjected += 1
        
        def hasMovingPoints(self):
            return len(self.movingPoints)>0
      
        def propagate(self):
            if self.hasMovingPoints():                
                pointsToKeep = []
                firstPoint = max(0,self.nbInjected-1)
                for d in self.movingPoints[firstPoint:]:
                    d += 1
                    if d>self.distanceToNext:
                        if self.nextNode.prevs.index(self.fromNode)==0:
                            self.nextNode.inject(d-self.distanceToNext)
                    else:
                        pointsToKeep.append(d)                    
                self.movingPoints = pointsToKeep
                self.nbInjected = 0
        
        def draw(self):
            glBegin(GL_POINTS)                
            for d in self.movingPoints:
                p = self.fromNode.p + d * self.dirToNext
                glVertex2fv(p)
            glEnd()


    class ExecutionGraphNode:
        def __init__(self, p, prevNodes,color):                
            self.p = p
            if color==1:
                self.color=[1,0,0,1]
            elif color==2:
                self.color=[0,1,0,1]
            elif color==3:
                self.color=[0,0,1,1]
            self.movingPointsDistance = []
            ScenarioExecution.totalsize += 1
            self.connexionsToNext = []
            self.prevs = []
            self.nexts = []
            for n in prevNodes:
                if n!=None:
                    if self not in n.nexts:
                        n.nexts.append(self)
                    if n not in self.prevs:
                        #if len(self.prevs)==0:
                        n.connexionsToNext.append(ScenarioExecution.ConnexionToNext(n, self))
                        self.prevs.append(n)

        def inject(self, d):
            for c in self.connexionsToNext:
                c.inject(d)             

        def propagate(self):
            for c in self.connexionsToNext:                    
                c.propagate()                 
            for c in self.connexionsToNext:
                if c.nextNode.prevs.index(self)==0:
                    c.nextNode.propagate()

        def hasMovingPoints(self):
            for c in self.connexionsToNext:
                if c.hasMovingPoints():
                    return True
            return False
        
        def draw(self):
            glLineWidth(2)
            glBegin(GL_LINES)            
            for n in self.nexts:
                #if n.prevs.index(self)==0:
                glColor4fv(self.color)                    
                glVertex2fv(self.p)
                glColor4fv(n.color)
                glVertex2fv(n.p)     
            glEnd()

            
            if self.hasMovingPoints():
                glColor4f(1,0,1,1)                    
                glPointSize(5)
                for c in self.connexionsToNext:
                    c.draw()

            for n in self.nexts:                                  
                if n.prevs.index(self)==0:
                    n.draw()

        def print(self,depth):            
            nextStr = ""
            for n in self.nexts:
                nextStr += str(n) + " "

            print(str(self) + " " + str(len(self.nexts)) + " " + nextStr)

            for n in self.nexts:
                if n.prevs.index(self)==0:
                    n.print(depth+1)            
                
        def size(self):
            s = 1

            for n in self.nexts:
                if n.prevs.index(self)==0:
                    s += n.size()
            return s
            
        def rootNode(self):
            if len(self.prevs)!=0:
                return self.prevs[0].rootNode()
            else:
                return self

    class ExecutionTree:
        def __init__(self, prev, connexion):                
            self.connexion = connexion
            self.prev = prev
            self.nexts = []
      
        def size(self):
            s = 1
            for n in self.nexts:
                s += n.size()
            return s
        
        def addSuccessor(self, connexion):
            successor = ScenarioExecution.ExecutionTree(self, connexion)
            self.nexts.append(successor)
            return successor
        
        def blink(self,b):
            self.connexion.attachementStart.node.geometry.setSelected(b)
            self.connexion.attachementEnd.node.geometry.setSelected(b)
            for n in self.nexts:
                n.blink(b)

        def onSegment(self, p, segment):

            d1 = np.linalg.norm(p-segment[0])
       
            if d1<=1e-8:
                return d1
       
            d2 = np.linalg.norm(p-segment[1])

            if d2<=1e-8:
               return -1
            
            d = np.linalg.norm(segment[0]-segment[1])            

            if fabs(d-d1-d2)<=1e-8:
                return d
            
            return -1
            

        def findNextEdge(self, point, polygon, initialPoint):
            prevVertex = polygon[0]
            for v in polygon[1:]:
                print("###########")
                print(self.connexion.attachementEnd.node.name)
                print(polygon)
                print(point)
                print([prevVertex, v])                
                print(self.onSegment(point, [prevVertex, v]))
                if self.onSegment(point, [prevVertex, v]) >= 0:                  
                    edge = [point, v]                                                        
                    print(edge)
                    
                    
                    dInitialPoint = self.onSegment(initialPoint, edge)
                    if dInitialPoint >= 1e-8: # if initial point is on next edge and is not first point of edge
                        edge[1] = initialPoint
                    print(edge)
                    print("###########")
                    return edge
                prevVertex = v
            assert(False)
            return None # should not happen
        
        def findPointsOnEdge(self, edge, outgoingConnexions):
            pointsDistance = []
            pointsOnEdge = []
            for c in outgoingConnexions:
                p = c.attachementStart.connexionPoint()
                d = self.onSegment(p, edge)            
                if d>=0:
                    pointsDistance.append(d)
                    pointsOnEdge.append([p, c])
            
            sortedPointsOnEdge = [x for _,x in sorted(zip(pointsDistance,pointsOnEdge))]          
            return sortedPointsOnEdge


        def perimeter(self, polygon):            
            if len(polygon)==0:
                 return 0
            p = 0
            prevVertex = polygon[0]
            for v in polygon[1:]:
                p += np.linalg.norm(prevVertex-v)
                prevVertex = v
            p += np.linalg.norm(prevVertex-polygon[0])
            return p
                

        def extractPath(self, fromPoint, polygon, outgoingConnexions):
            path = [[fromPoint, None]]                                    
            while len(path)==1 or np.linalg.norm(fromPoint-path[-1][0]) > 1e-8: # while last point on path is not first point
                edge =self.findNextEdge(path[-1][0], polygon, fromPoint)                 
                pointsOnEdge = self.findPointsOnEdge(edge, outgoingConnexions)
                print("pointsOnEdge= "+str(pointsOnEdge))
                if len(pointsOnEdge)!=0:
                    path += pointsOnEdge
                path.append([edge[1],None])
            return path

        def getSubPath(self, path, maxLength):
            subPathLength = 0
            subPath =  [path[0]]
            for p in path[1:]:
                subPath.append(p)
                subPathLength += np.linalg.norm(subPath[-1][0]-subPath[-2][0])
                if p[1] != None and subPathLength > maxLength-1e-8 :                        
                    return subPath
            return subPath
    
        def getOtherSubPath(self, path, lastPoint):
            subPath = []
            for p in reversed(path):                
                subPath.append(p)
                if np.linalg.norm(p[0]-lastPoint)<1e-8:
                    return subPath 
            return subPath
            
        def splitInTwoPathes(self, fromPoint, polygon, outgoingConnexions):
            path = self.extractPath(fromPoint, polygon, outgoingConnexions) 
            print("path = "+str(path))
            print("polygon = "+str(polygon))      
            polygonPerimeter = self.perimeter(polygon)

            path1 = self.getSubPath(path, polygonPerimeter/2)                      
            print("path1 = "+str(path1))      

            path2 = self.getOtherSubPath(path,path1[-1][0])                      
            print("path2 = "+str(path2))      
            
            return path1,path2

        def findNext(self, connexion):
            for n in self.nexts:
                if n.connexion == connexion:
                    return n
            return None
        
        def extractGraphFromPath(self, path, prevNode,color):
            lastNode = prevNode
            for p in path[1:-1]:
                outgoingConnexion = p[1]
                if outgoingConnexion==None:
                    lastNode = ScenarioExecution.ExecutionGraphNode(p[0], [lastNode],color)
                else:
                    next = self.findNext(outgoingConnexion)
                    if next!=None:# and next.connexion.attachementEnd.node.name != "doStart":
                        lastNode = next.extractGraph(lastNode)
                        print("blahblah")
            return lastNode
            
        def extractGraph(self, prevExecutionGraphNode):
            
            points = self.connexion.arrow.getPoints()    
            firstConnexionNode = ScenarioExecution.ExecutionGraphNode(points[0], [prevExecutionGraphNode], 1)
            lastConnexionNode = firstConnexionNode
            for p in points[1:]:
                lastConnexionNode = ScenarioExecution.ExecutionGraphNode(p, [lastConnexionNode], 1)

            contourPoints = self.connexion.attachementEnd.getConnexionRectangle()
            contourPoints.append(contourPoints[0])

            # tow path starting and ending with same point or one is empty
            path1, path2 = self.splitInTwoPathes(points[-1], contourPoints, self.connexion.attachementEnd.node.outgoingArrows)
            
            lastNode1 = self.extractGraphFromPath(path1, lastConnexionNode,2)            
            if len(path2)>1: 
                lastNode2 = self.extractGraphFromPath(path2, lastConnexionNode,3)   
                lastNode = ScenarioExecution.ExecutionGraphNode(path1[-1][0], [lastNode1,lastNode2],1)                                                
            else: # no outgoing connexion, path1 is the full contour of polygon
                lastNode = ScenarioExecution.ExecutionGraphNode(path1[-1][0], [lastNode1],1)
            #lastNode = ScenarioExecution.ExecutionGraphNode(path1[-1][0], [lastNode1],1)
            if path1[-1][1] == None:
                return firstConnexionNode
            else:
                next = self.findNext(path1[-1][1])
                if next!=None:# and next.connexion.attachementEnd.node.name != "doStart":
                    next.extractGraph(lastNode)                
                return firstConnexionNode
            

    def __init__(self, node):
        self.iter = 0
        self.stop = node==None or len(node.outgoingArrows)==0
        if not self.stop:
            self.executionTree = ScenarioExecution.ExecutionTree(None, node.outgoingArrows[0])
            newExecutionNode = self.executionTree
            while newExecutionNode!=None:
                newExecutionNode = self.addNextConnexionToFollow(newExecutionNode)
            self.executionGraph = self.executionTree.extractGraph(None)
            #self.executionGraph = self.executionGraph.rootNode()
        else:
            self.stop = True

        print("Execution tree size = "+str(self.executionTree.size()))
        print("Execution graph size = "+str(self.executionGraph.size()))
        print("Execution graph size = "+str(ScenarioExecution.totalsize))
        self.executionGraph.print(0)
        

    def addNextConnexionToFollow(self, prevExecutionNode):
                
        executionNode = prevExecutionNode
        while executionNode!=None:
            node = executionNode.connexion.attachementEnd.node        
            connexionsVisited = len(executionNode.nexts)
            totalConnexions = len(node.outgoingArrows)
            if connexionsVisited < totalConnexions:
                return executionNode.addSuccessor(node.outgoingArrows[connexionsVisited])
            executionNode = executionNode.prev
        return None
    
    def next(self):
        #if int(self.iter/10)%2 == 0:
        #    self.executionTree.blink(-1)
        #else:
        #    self.executionTree.blink(0)

        if self.iter%10 == 0:
            self.executionGraph.inject(0)

        self.executionGraph.propagate()
        self.iter += 1        

    def draw(self):
        self.executionGraph.draw()
