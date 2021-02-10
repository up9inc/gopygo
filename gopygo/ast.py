#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: __init__
    :synopsis: Go AST classes.
"""

from typing import List, Union


class Package():
    def __init__(self, name: str):
        self.name = name
        self.imports = []
        self.decls = []


class ImportSpec():
    def __init__(self, path: Union[str, List[str]]):
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
    def __init__(self, fun: str, args: list, chain=None):
        self.fun = fun
        self.args = args
        self.chain = chain  # TODO: Is that correct to have this in here?


class ValueSpec():
    def __init__(self, names: list, _type: str, values: list, decl=None):
        self.names = names
        self.type = _type
        self.values = values
        self.decl = decl


class Comment():
    def __init__(self, text: str):
        self.text = text


class Stmt():
    def __init__(self, expr):
        self.expr = expr


class AssignStmt():
    def __init__(self, lhs: list, token: str, rhs: list):
        self.lhs = lhs
        self.token = token
        self.rhs = rhs


class ReturnStmt():
    def __init__(self, results: List[str]):
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
