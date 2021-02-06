class Package():
    def __init__(self, name):
        self.name = name
        self.imports = []
        self.decls = []


class ImportSpec():
    def __init__(self, path):
        self.path = path


class FuncDecl():
    def __init__(self, _type, name, params, body):
        self.type = _type
        self.name = name
        self.params = params
        self.body = body


class SelectorExpr():
    def __init__(self, x, sel):
        self.x = x
        self.sel = sel


class CallExpr():
    def __init__(self, fun, args):
        self.fun = fun
        self.args = args


class ValueSpec():
    def __init__(self, _type, value):
        self._type = _type
        self.value = value


class Comment():
    def __init__(self, text):
        self.text = text
