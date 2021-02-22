#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: __init__
    :synopsis: Go AST classes.
"""

from typing import List, Union


class Ident():
    def __init__(self, name: str):
        self.name = name


class BasicLit():
    def __init__(self, kind, value: Union[str, None]):
        self.kind = kind
        self.value = value


class CompositeLit():
    def __init__(self, _type, elts: list, incomplete: bool):
        self.type = _type
        self.elts = elts
        self.incomplete = incomplete


class GenDecl():
    def __init__(self, tok: str, specs: list):
        self.tok = tok
        self.specs = specs


class DeclStmt():
    def __init__(self, decl: GenDecl):
        self.decl = decl


class Package():
    def __init__(self, name: str):
        self.name = name


class File():
    def __init__(self, name: Package):
        self.name = name
        self.imports = []  # unused, use GenDecl in self.decls instead
        self.decls = []


class ImportSpec():
    def __init__(self, name: Union[Ident, str, None], path: Union[BasicLit, List[BasicLit]]):
        self.name = name
        self.path = path


class Field():
    def __init__(self, name: str, _type):
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
    def __init__(self, name: str, _type: FuncType, body: BlockStmt, recv=None):
        self.name = name
        self.type = _type
        self.body = body
        self.recv = recv


class SelectorExpr():
    def __init__(self, x: str, sel: str):
        self.x = x
        self.sel = sel


class CallExpr():
    def __init__(self, fun: str, args: list, ellipsis=False):
        self.fun = fun
        self.args = args
        self.ellipsis = ellipsis


class ArrayType():
    def __init__(self, _len, elt: str):
        self.len = _len
        self.elt = elt


class ValueSpec():
    def __init__(self, names: list, _type: Union[str, ArrayType], values: list):
        self.names = names
        self.type = _type
        self.values = values


class Comment():
    def __init__(self, text: str):
        self.text = text


class ExprStmt():
    def __init__(self, expr):
        self.expr = expr


class AssignStmt():
    def __init__(self, lhs: list, token: str, rhs: list):
        self.lhs = lhs
        self.token = token
        self.rhs = rhs


class FuncLit():
    def __init__(self, _type: FuncType, body: BlockStmt):
        self.type = _type
        self.body = body


class ReturnStmt():
    def __init__(self, results: List[Union[str, FuncLit]]):
        self.results = results


class BinaryExpr():
    def __init__(self, x, op: str, y):
        self.x = x
        self.op = op
        self.y = y


class UnaryExpr():
    def __init__(self, op: str, x, right=False):
        self.op = op
        self.x = x
        self.right = right


class ParenExpr():
    def __init__(self, x):
        self.x = x


class ForStmt():
    def __init__(self, body: BlockStmt, init=None, cond=None, post=None):
        self.init = init
        self.cond = cond
        self.post = post
        self.body = body


class BranchStmt():
    def __init__(self, tok: str, label=None):
        self.tok = tok
        self.label = label


class LabeledStmt():
    def __init__(self, label: str):
        self.label = label


class IfStmt():
    def __init__(self, cond, body: BlockStmt, init=None, _else=None):
        self.init = init
        self.cond = cond
        self.body = body
        self._else = _else


class SwitchStmt():
    def __init__(self, body: BlockStmt, init=None, tag=None):
        self.init = init
        self.tag = tag
        self.body = body


class CaseClause():
    def __init__(self, _list: list, body: list):
        self.list = _list
        self.body = body


class IndexExpr():
    def __init__(self, x, index):
        self.x = x
        self.index = index


class TypeAssertExpr():
    def __init__(self, x, _type):
        self.x = x
        self.type = _type


class SliceExpr():
    def __init__(self, x, low, high, _max, slice3: bool):
        self.x = x
        self.low = low
        self.high = high
        self.max = _max
        self.slice3 = slice3


class MapType():
    def __init__(self, key, value):
        self.key = key
        self.value = value


class KeyValueExpr():
    def __init__(self, key, value):
        self.key = key
        self.value = value


class RangeStmt():
    def __init__(self, key, value, tok: str, x, body: BlockStmt):
        self.key = key
        self.value = value
        self.tok = tok
        self.x = x
        self.body = body


class Ellipsis():
    def __init__(self, _type: str):
        self.type = _type


class StarExpr():
    def __init__(self, x):
        self.x = x


class StructType():
    def __init__(self, fields: FieldList, incomplete: bool):
        self.fields = fields
        self.incomplete = incomplete


class TypeSpec():
    def __init__(self, name: Ident, _type):
        self.name = name
        self.type = _type


class InterfaceType():
    def __init__(self, methods: FieldList, incomplete: bool):
        self.methods = methods
        self.incomplete = incomplete
