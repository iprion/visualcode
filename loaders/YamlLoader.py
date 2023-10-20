from loaders.NodeInstanceBuilder import *
from loaders.Loader import *
import yaml

class YamlLoader(Loader):
    
    def load(self, path, fileName):
        self.fileName = fileName
        self.path = path
        fullPath = path + "/" + fileName + ".yml"
        self.rootNodeConf = {}
        try:
            with open(fullPath, 'r') as file:
                docs = yaml.safe_load_all(file)            
                for doc in docs:                
                    self.rootNodeConf = doc
        except:
            print("No config found")
            return False
        
        return True
       
    def generate(self):
        root = self.createNode(None, self.rootNodeConf)
        return root
    
    def extractFields(self, conf, className):
        fields = conf[className].copy()
        if "subNodes" in fields:
            fields.pop("subNodes")
        return fields
        
    def createNode(self, parentNode, conf):        
        
        if len(conf)==0:
            return None
        
        className = list(conf.keys())[0]        
        fields = self.extractFields(conf, className)            
        nodeName = conf[className]["name"]
        newNode = NodeInstanceBuilder.createNodeInstance(parentNode, className, nodeName, fields)

        print("  "*newNode.depthInModuleHierarchy + newNode.name + " creation STARTED")

        internalConf = conf[className]
        self.loadNodeConf(newNode, internalConf)

        print("  "*newNode.depthInModuleHierarchy + newNode.name + " creation DONE")

        return newNode
    
    def loadNodeConf(self, node, internalConf):
                
        if "color" in internalConf:
            node.backgroundColor = internalConf["color"]
            print("  "*(node.depthInModuleHierarchy+1) + " loading color")    
        else:
            if node.parentNode != None:
                node.backgroundColor = node.parentNode.backgroundColor
                node.backgroundColor[3] = min(1,node.parentNode.backgroundColor[3]*1.5)
                print("  "*(node.depthInModuleHierarchy+1) + " color not found")        

        if "subNodes" in internalConf:
            self.loadSubNodesConf(node, internalConf["subNodes"])        

       
    def loadSubNodesConf(self, parentNode,conf):        
        for subConf in conf:
            subNode = self.createNode(parentNode, subConf)
            if len(parentNode.subNodes) != 0:
                prevSibling = parentNode.subNodes[len(parentNode.subNodes)-1]
                subNode.prevSibling = prevSibling
                prevSibling.nextSibling = subNode
            parentNode.subNodes.append(subNode)
