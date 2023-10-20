class NodeInstanceBuilder():

    ast2visualcode = {
        "ClassDefinition":"ClassDefinition",
        "FunctionDefinition":"FunctionDefinition",
        "ClassDef":"ClassDefinition",
        "FunctionDef":"FunctionDefinition",
        "Module":"RootDefinition",
        "FunctionCall":"FunctionCall",
        "Assign":"Assign",
        "Name":"Name",
        "Store":"Store",
        "Constant":"Constant",
        "arguments":"arguments",
        "arg":"arg",
        "Call":"Call",
        "Attribute":"Attribute",
        "Load":"Load",
        "Expr":"Expr",
        "Return":"Return",
        "Pass":"Pass",
        "List":"List",
        "Import":"Import",
        "alias":"Alias",
        "If":"If",
        "Compare":"Compare",
        "Eq":"Eq",
        "For":"For",
        "BinOp":"BinOp",
        "Add":"Add"
    }

    def createNodeInstance(parentNode, className, nodeName, fields):      
         
        from definitions.FunctionDefinition import FunctionDefinition as FunctionDefinition
        from definitions.ClassDefinition import ClassDefinition as ClassDefinition
        from definitions.FunctionCall import FunctionCall as FunctionCall
        from definitions.RootDefinition import RootDefinition as RootDefinition
        from loaders.PythonLoader import ClassDef as ClassDef
        from loaders.PythonLoader import Assign as Assign
        from loaders.PythonLoader import Name as Name
        from loaders.PythonLoader import Store as Store
        from loaders.PythonLoader import Constant as Constant
        from loaders.PythonLoader import FunctionDef as FunctionDef
        from loaders.PythonLoader import arguments as arguments
        from loaders.PythonLoader import arg as arg
        from loaders.PythonLoader import Call as Call
        from loaders.PythonLoader import Attribute as Attribute
        from loaders.PythonLoader import Load as Load
        from loaders.PythonLoader import Expr as Expr
        from loaders.PythonLoader import Return as Return
        from loaders.PythonLoader import Pass as Pass
        from loaders.PythonLoader import List as List
        from loaders.PythonLoader import Import as Import
        from loaders.PythonLoader import Alias as Alias
        from loaders.PythonLoader import If as If
        from loaders.PythonLoader import Compare as Compare
        from loaders.PythonLoader import Eq as Eq
        from loaders.PythonLoader import For as For
        from loaders.PythonLoader import BinOp as BinOp
        from loaders.PythonLoader import Add as Add

        klass = locals()[NodeInstanceBuilder.ast2visualcode[className]]
        return klass(nodeName, parentNode, fields)

    
