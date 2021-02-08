#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: __init__
    :synopsis: Go unparser (code generator) module.
"""

import re

INDENT = '    '

camel_to_snake_pattern = re.compile(r'(?<!^)(?=[A-Z])')


def _camel_to_snake(string):
    return camel_to_snake_pattern.sub('_', string).lower()


def _get_node_type(object):
    return _camel_to_snake(object.__class__.__name__)


class Generator():
    def __init__(self):
        self.indent = 0

    def package(self, node):
        text = 'package %s\n' % node.name

        if node.imports:
            text += '\n'
        for _import in node.imports:
            text += self._import(_import)
        if node.decls:
            text += '\n'

        for decl in node.decls:
            text += getattr(self, _get_node_type(decl))(decl)
        return text.rstrip() + '\n'

    def _import(self, node):
        text = 'import %s\n' % node.path
        return text

    def func_decl(self, node):
        text = 'func %s' % node.name
        text += getattr(self, _get_node_type(node.type))(node.type)
        text += ' '
        text += getattr(self, _get_node_type(node.body))(node.body)
        return text

    def func_type(self, node):
        text = '(%s)' % getattr(self, _get_node_type(node.params))(node.params)

        if node.results.list:
            text += ' '
            if len(node.results.list) > 1:
                text += '('
            text += '%s' % getattr(self, _get_node_type(node.results))(node.results)
            if len(node.results.list) > 1:
                text += ')'
        return text

    def field_list(self, node):
        text = ''
        for field in node.list:
            text += '%s, ' % getattr(self, _get_node_type(field))(field)
        if node.list:
            text = text[:-2]
        return text

    def field(self, node):
        if node.name is None:
            return '%s' % node.type
        else:
            return '%s %s' % (node.name, node.type)

    def block_stmt(self, node):
        text = '{\n'
        self.indent += 1
        for stmt in node.list:
            text += getattr(self, _get_node_type(stmt))(stmt)
        self.indent -= 1
        text += '}\n\n'
        return text

    def selector_expr(self, node):
        text = '%s.%s' % (
            node.x,
            getattr(self, _get_node_type(node.sel))(node.sel)
        )
        return text

    def call_expr(self, node):
        text = '%s(' % node.fun
        for arg in node.args:
            text += '%s, ' % getattr(self, _get_node_type(arg))(arg)
        if node.args:
            text = text[:-2]
        text += ')'
        return text

    def value_spec(self, node):
        text = ''
        if node.names:
            text += 'var '
        for name in node.names:
            text += '%s, ' % name
        if node.names:
            text = text[:-2]
        for value in node.values:
            text += '%s, ' % value
        if node.values:
            text = text[:-2]
        if node.type is not None:
            text += ' %s' % node.type
        return text

    def comment(self, node):
        return '// %s' % node.text

    def str(self, node):
        return node

    def stmt(self, node):
        return '%s%s\n' % (
            self.indent * INDENT,
            getattr(self, _get_node_type(node.expr))(node.expr)
        )

    def assign_stmt(self, node):
        lhs = ''
        for _node in node.lhs:
            lhs += '%s, ' % getattr(self, _get_node_type(_node))(_node)
        if node.lhs:
            lhs = lhs[:-2]
        rhs = ''
        for _node in node.rhs:
            rhs += '%s, ' % getattr(self, _get_node_type(_node))(_node)
        if node.rhs:
            rhs = rhs[:-2]
        return '%s%s %s %s\n' % (
            self.indent * INDENT,
            lhs,
            node.token,
            rhs
        )

    def return_stmt(self, node):
        text = '%sreturn ' % (self.indent * INDENT)
        for result in node.results:
            text += '%s, ' % getattr(self, _get_node_type(result))(result)
        if node.results:
            text = text[:-2]
        text += '\n'
        return text

    def binary_expr(self, node):
        x = node.x
        x = getattr(self, _get_node_type(x))(x) if not isinstance(x, str) else x
        y = node.y
        y = getattr(self, _get_node_type(y))(y) if not isinstance(y, str) else y
        return '%s %s %s' % (
            x,
            node.op,
            y
        )

    def unary_expr(self, node):
        x = node.x
        x = getattr(self, _get_node_type(x))(x) if not isinstance(x, str) else x
        return '%s %s' % (
            node.op,
            x
        )

    def paren_expr(self, node):
        x = node.x
        x = getattr(self, _get_node_type(x))(x) if not isinstance(x, str) else x
        return '(%s)' % x


def unparse(tree):
    generator = Generator()
    return getattr(generator, _get_node_type(tree))(tree)
