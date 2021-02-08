#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: __init__
    :synopsis: Go AST classes.
"""

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
    def __init__(self, names: list, _type: str, values: list, is_decl=False):
        self.names = names
        self.type = _type
        self.values = values
        self.is_decl = is_decl


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
    def __init__(self, op: str, x):
        self.op = op
        self.x = x


class ParenExpr():
    def __init__(self, x):
        self.x = x
