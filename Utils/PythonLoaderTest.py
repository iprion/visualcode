from ast import *

class ASTNode():
    
    identifiers = ["name", "module", "names", "attr", "id", "arg", "asname", "rest", "kwd_attrs"]

    def __init__(self, parent, type, depth):
        self.depth = depth 
        self.type = type
        self.subNodes = []
        self.fields = {}
        self.parent = parent


    def load(self, path, fileName):
        self.fileName = fileName
        self.path = path
        fullPath = path + "/" + fileName
        with open(fullPath, 'r') as file:
            fileContent = file.read() 
            node = parse(fileContent, fileName)    
            self.visit(node)
    
    def dump(self, root): 
        pass                            


    def visit(self, node):
        self.node = node
        self.extractFields()
        for field, value in iter_fields(node):            
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, AST):
                        self.addSubNode(item)                        
            elif isinstance(value, AST):
                self.addSubNode(value)


    def addSubNode(self, item):
        className = item.__class__.__name__
        subM = ASTNode(item, className, self.depth+1)               
        self.subNodes.append(subM)
        subM.visit(item)
        
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
            
    def node2str2(self,node):
        if isinstance(node, AST):
            fields = [(name, self.node2str(val)) for name, val in iter_fields(node) if name not in ('left', 'right')]
            rv = node.__class__.__name__
            for field in fields:
                if field[0] in self.identifiers or field[0]=="value" and "(" not in field[1]:
                    rv += " " + field[0]+"="+field[1]
            return rv
        else:
            return repr(node)
        
    def extractFields(self):
        if isinstance(self.node, AST):
            self.fields = {name : self.node2str(val) for name, val in iter_fields(self.node) if name not in ('left', 'right')}
        else:
            self.fields = {}

    def astTree(self):
        lines = [self.offsetStr('--', self.node2str2(self.node))]
        for s in self.subNodes:
            lines.append(s.astTree())
        return self.joinLines(lines, "\n")

    def value(self, fieldName, stripQuote=False):
        if fieldName in self.fields:
            v = self.fields[fieldName]
            if stripQuote and v[0] == "'" and v[-1] == "'" :
                return v[1:-1]
            else:
                return v
        else:
            return "####"

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

parser = ASTNode(None, "ROOT", 0)
parser.load("projects", "solrv2.py")
print(parser.astTree())
