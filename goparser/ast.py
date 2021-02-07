from typing import List


class Package():
    def __init__(self, name: str):
        self.name = name
        self.imports = []
        self.decls = []


class ImportSpec():
    def __init__(self, path: str):
        self.path = path


class Field():
    def __init__(self, name: str, _type: str):
        self.name = name
        self.type = _type


class FieldList():
    def __init__(self, _list: List[Field]):
        self.list = _list


class FuncType():
    def __init__(self, params: FieldList, results: FieldList):
        self.params = params
        self.results = results


class BlockStmt():
    def __init__(self, _list: list):
        self.list = _list


class FuncDecl():
    def __init__(self, name: str, _type: FuncType, body: BlockStmt):
        self.name = name
        self.type = _type
        self.body = body


class SelectorExpr():
    def __init__(self, x: str, sel: str):
        self.x = x
        self.sel = sel


class CallExpr():
    def __init__(self, fun: str, args: list):
        self.fun = fun
        self.args = args


class ValueSpec():
    def __init__(self, _type: str, value):
        self._type = _type
        self.value = value


class Comment():
    def __init__(self, text: str):
        self.text = text


class Stmt():
    def __init__(self, expr):
        self.expr = expr


class AssignStmt():
    def __init__(self, lhs: str, token: str, rhs):
        self.lhs = lhs
        self.token = token
        self.rhs = rhs
