from loaders.NodeInstanceBuilder import NodeInstanceBuilder
from loaders.Loader import Loader

from definitions.FunctionCall import FunctionCall as FunctionCall
from definitions.ClassDefinition import ClassDefinition as ClassDefinition
from definitions.FunctionDefinition import FunctionDefinition as FunctionDefinition
from definitions.RootDefinition import RootDefinition as RootDefinition
from ast import *
import numpy as np

class PythonLoader(Loader):

    def load(self, path, fileName):

        self.fileName = fileName
        self.path = path
        fullPath = path + "/" + fileName + ".py"
        self.rootNodeConf = {}
        self.rootNodeLayoutConf = {}
        
        try:
            with open(fullPath, 'r') as file:
                fileContent = file.read() 
                self.rootNodeConf = parse(fileContent, fileName)#, mode='single')    
        except:
            print("No config found")
            return False  
        return True     
    
    def dump(self, root): 
        pass                            
   
    def generate(self):
        root = self.createNode(None, self.rootNodeConf)
        self.extractName(root)

        return root
    
    def loadNodeConfWithGeometry(self, node, nodeConf, withGeometry):

        self.extractBackgroundColor(node)

        for field, value in iter_fields(nodeConf):            
            
            values = []
            
            if isinstance(value, list):
                values = value
            elif isinstance(value, AST):  
                values = [value]
            
            for subNodeConf in values:               
                newNode = self.createNodeInstance(node, subNodeConf)
                if withGeometry == newNode.hasGeometry():
                    self.loadSubNodeConf(node, subNodeConf)     

    def loadNodeConf(self, node, nodeConf):        

        self.loadNodeConfWithGeometry(node, nodeConf, False)                    
        self.loadNodeConfWithGeometry(node, nodeConf, True)

    def createNodeInstance(self, parentNode, conf):
        className = conf.__class__.__name__
        fields = self.extractFields(conf)
        nodeName = self.value(fields, "name", True, className)
        return NodeInstanceBuilder.createNodeInstance(parentNode, className, nodeName, fields)

    def createNode(self, parentNode, conf):                
        
        newNode = self.createNodeInstance(parentNode, conf)

        print("  "*newNode.depthInModuleHierarchy + newNode.name + " creation STARTED")

        self.loadNodeConf(newNode, conf)

        print("  "*newNode.depthInModuleHierarchy + newNode.name + " creation DONE")

        if isinstance(newNode, Expr):
            print("  "*newNode.depthInModuleHierarchy + "Expr conversion to FunctionCall")
            functionCalled = newNode.python()
            functionCall = NodeInstanceBuilder.createNodeInstance(parentNode, "FunctionCall", functionCalled, {})
            if newNode.prevSibling != None:
                functionCall.prevSibling = newNode.prevSibling
                functionCall.prevSibling.nextSibling = functionCall
            if newNode.nextSibling != None:    
                functionCall.nextSibling = newNode.nextSibling
                functionCall.nextSibling.prevSibling = functionCall
            functionCall.backgroundColor = newNode.backgroundColor

            newNode = functionCall
        elif isinstance(newNode, ClassDefinition): # can handle color also
            attributes =  self.getSubNodes(newNode, [Assign], {}) 
            for a in attributes:
                assignedVarNodes = self.getSubNodes(a, [Name], {}) 
                if len(assignedVarNodes) == 1:
                    assignedVarName = assignedVarNodes[0].value("id", True)
                    assignedValueNodes = self.getSubNodes(a, [Call], {}) 
                if len(assignedValueNodes) == 1:
                    assignedValue = assignedValueNodes[0].python()
                    newNode.addAttribute(assignedVarName, assignedValue, FunctionCall)
                #else: 
                #    assignedValueNode = self.getSubNode(newNode, [Assign, Constant], {}) 
                #    if assignedValueNode!=None: 
                #        assignedValue = assignedValueNode.python()
                #        newNode.addAttribute(assignedVarName, assignedValue, Constant)
                #    else:
                #        assignedValueNode = self.getSubNode(newNode, [Assign, List], {}) 
                #        if assignedValueNode!=None:
                #            assignedValue = assignedValueNode.python()
                #            newNode.addAttribute(assignedVarName, assignedValue, List)
        return newNode

    def loadSubNodeConf(self, parentNode,subNodeConf):        
        subNode = self.createNode(parentNode, subNodeConf)
        if subNode == None:
            return 

        if len(parentNode.subNodes) != 0:
            prevSibling = parentNode.subNodes[len(parentNode.subNodes)-1]
            subNode.prevSibling = prevSibling
            prevSibling.nextSibling = subNode            

        if subNode.hasGeometry() or not parentNode.hasGeometry():            
            parentNode.subNodes.append(subNode)
        else:
            parentNode.noGeometrySubNodes.append(subNode)
                
    def extractBackgroundColor(self, node):
        
        #if type(node)!=ClassDefinition and type(node)!=FunctionDefinition:
        #    return
        
        if node.parentNode != None:
            node.backgroundColor = node.parentNode.backgroundColor.copy()
            node.backgroundColor[3] = min(1,node.parentNode.backgroundColor[3]*1.5)   

        colorNodes = self.getSubNodes(node, [Assign, Name], {'id':'color'})
        if len(colorNodes)==1:
            listNodes = self.getSubNodes(colorNodes[0].parentNode, [List])
            if len(listNodes)==1:
                color = listNodes[0].toList()                
                if len(color)==4:
                    node.backgroundColor = [color[0]/255.0,color[1]/255.0,color[2]/255.0,color[3]]
        
        c = node.backgroundColor
        print("  "*node.depthInModuleHierarchy +"background color is [" + str(c[0]) + ", " + str(c[1]) + ", "+ str(c[2]) + ", "+ str(c[3]) + "]")
    

    def extractName(self, node):
        
        if type(node)!=RootDefinition:
            return "###"
        
        #print('extractName for '+node.name, file=sys.stderr)
        nameNodes = self.getSubNodes(node, [Assign, Name], {'id':'AppName'})        
        if len(nameNodes)==1:
            #print('extractName for '+node.name + " nameNode Found", file=sys.stderr)
            nameValueNodes = self.getSubNodes(nameNodes[0].parentNode, [Constant])
            if len(nameValueNodes)==1:
                #print('extractName for '+node.name + " nameValueNode Found "+nameValueNode.python() , file=sys.stderr)
                node.name = nameValueNodes[0].python()                                

    def getSubNodes(self, node, typeChain, params={}):

        if len(typeChain)==0:
            for pname in params:
                pRequiredValue = params[pname]
                actualValue = node.value(pname, True, None)
                #print(pname + " =? " + pRequiredValue + "   ----   " + actualValue)
                if actualValue != pRequiredValue:
                    return []
            return [node]

        requiredType = typeChain.pop(0)        
        subNodes = node.noGeometrySubNodes if node.hasGeometry() else node.subNodes
        foundNodes = []
        #print(str(typeChain) + str(params), file=sys.stderr)
        for subNode in subNodes:
            #print(str(requiredType) + "   ----   " + str(type(subNode)), file=sys.stderr)
            if type(subNode) == requiredType:
                foundSubNodes = self.getSubNodes(subNode, typeChain, params)
                if len(foundSubNodes)!=0:
                    foundNodes = foundNodes + foundSubNodes
        return foundNodes

    def value(self, fields, fieldName, stripQuote, defaultValue="####"):
        if fieldName in fields:
            v = fields[fieldName]
            if stripQuote and v[0] == "'" and v[-1] == "'" :
                return v[1:-1]
            else:
                return v
        else:
            return defaultValue
        
    def extractFields(self, node):
        if isinstance(node, AST):
            return {name : self.node2str(val) for name, val in iter_fields(node) if name not in ('left', 'right')}
        else:
            return {}        

    def printOffset(self, space, str):
        print(self.offsetStr(space,str))

    def offsetStr(self, space, str):
        return space*self.depth+str

    def getsubNodes(self, type):
        subNodes = []
        for s in self.subNodes:
            if s.type == type:
                subNodes.append(s)
        return subNodes

    def joinLines(self, lines, sep):
        return sep.join([line for line in lines if line != None])       
                
    def node2str(self,node):
        if isinstance(node, AST):
            fields = [(name, self.node2str(val)) for name, val in iter_fields(node) if name not in ('left', 'right')]
            rv = '%s(%s' % (node.__class__.__name__, ', '.join('%s=%s' % field for field in fields))
            return rv + ')'
        else:
            return repr(node)
        
    def astTree(self):
        lines = [self.offsetStr('--', self.node2str(self.node))]
        for s in self.subNodes:
            lines.append(s.astTree())
        return self.joinLines(lines, "\n")

    def yaml(self):
        lines = [self.offsetStr('  ', self.type)]
        for s in self.subNodes:
            print(s.type)
            lines.append(s.yaml())
        return self.joinLines(lines, "\n")
    
    def python(self):
        lines = []
        if self.type=='ROOT':
            for s in self.subNodes:
                lines.append(s.python())
        else:
            lines.append(self.offsetStr('  ', self.type))
        return self.joinLines(lines, "\n")  

class ASTNode():
    
    def __init__(self, name, parent, fields):
        self.name = name
        self.parentNode = parent
        self.fields = fields
        self.subNodes = []
        self.prevSibling = None
        self.nextSibling = None
        self.depthInModuleHierarchy = self.getDepth()
        self.backgroundColor = [187,187,187,1] #LIGHT_GREY
           
    def getDepth(self):
        parent = self.parentNode        
        depth = 0
        while parent!=None:
            depth += 1
            parent = parent.parentNode
        return depth
    
    def python(self):
        return __class__.__name__
        
    def value(self, fieldName, stripQuote=False, defaultValue = None):
        if fieldName in self.fields:
            v = self.fields[fieldName]
            if stripQuote and v[0] == "'" and v[-1] == "'" :
                return v[1:-1]
            else:
                return v
        else:
            return defaultValue
    
    def hasGeometry(self):
        return False
    
class Interactive(ASTNode):
    pass

class ClassDef(ASTNode):
    pass

class Assign(ASTNode):

    def python(self):
        var = self.subNodes[0].python()
        value = self.subNodes[1].python()
        return var+" = "+value

class Name(ASTNode):

    def python(self):
        return self.value('id', True)

class Store(ASTNode):
    pass

class Constant(ASTNode):

    def python(self):
        return self.value('value', True)

class FunctionDef(ASTNode):    
    pass
    
class arguments(ASTNode):
    pass

class arg(ASTNode):

    def python(self):
       return self.value("arg", True)

class Call(ASTNode):
    
    def python(self):
       return self.subNodes[0].python()

class Attribute(ASTNode):
    
    def python(self):
        return self.subNodes[0].python() + "." + self.value("attr", True)

class Load(ASTNode):
    pass

class Expr(ASTNode):

    def python(self):
       return self.subNodes[0].python()

class Return(ASTNode):
    pass

class List(ASTNode):
    def toList(self):
        l = []
        for s in self.subNodes:
            if type(s)==Constant:
                print(s.fields["value"])
                l.append(float(s.fields["value"]))
        return l

class Pass(ASTNode):
    pass

class Import(ASTNode):
    pass

class Alias(ASTNode):
    pass

class If(ASTNode):
    pass

class Compare(ASTNode):
    pass

class Eq(ASTNode):
    pass

class For(ASTNode):
    pass

class BinOp(ASTNode):
    pass

class Add(ASTNode):
    pass
