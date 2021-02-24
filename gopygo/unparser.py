#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: __init__
    :synopsis: Go unparser (code generator) module.
"""

import re

from gopygo.enums import Token
from gopygo.ast import Ident, FuncType

INDENT = '    '

camel_to_snake_pattern = re.compile(r'(?<!^)(?=[A-Z])')


def _camel_to_snake(string):
    return camel_to_snake_pattern.sub('_', string).lower()


def _get_node_type(object):
    return _camel_to_snake(object.__class__.__name__)


class Generator():
    def __init__(self):
        self.indent = 0

    def file(self, node):
        text = getattr(self, _get_node_type(node.name))(node.name)

        if node.decls:
            text += '\n'

        for decl in node.decls:
            text += getattr(self, _get_node_type(decl))(decl)
        return text.rstrip() + '\n'

    def package(self, node):
        return 'package %s\n' % node.name

    def import_spec(self, node):
        text = ''
        if node.name is not None:
            text += '%s ' % getattr(self, _get_node_type(node.name))(node.name)
        text += '%s\n' % getattr(self, _get_node_type(node.path))(node.path)
        return text

    def func_decl(self, node):
        text = 'func %s%s' % (
            ('(%s) ' % getattr(self, _get_node_type(node.recv))(node.recv)) if node.recv is not None else '',
            node.name
        )
        text += getattr(self, _get_node_type(node.type))(node.type)
        text += ' '
        text += getattr(self, _get_node_type(node.body))(node.body)
        text = text.rstrip() + '\n\n'
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

    def field_list(self, node, separator=', ', indent=''):
        text = ''
        for field in node.list:
            text += '%s%s%s' % (
                indent,
                getattr(self, _get_node_type(field))(field),
                separator
            )
        if node.list:
            text = text[:-len(separator)]
        return text

    def field(self, node):
        text = ''
        if node.name is None:
            if isinstance(node.type, FuncType):
                text += 'func'
            text += '%s' % getattr(self, _get_node_type(node.type))(node.type)
        else:
            gap = ' '
            if isinstance(node.type, FuncType):
                gap = ''
            text += '%s%s%s' % (
                node.name,
                gap,
                getattr(self, _get_node_type(node.type))(node.type)
            )
        return text

    def block_stmt(self, node):
        text = '{\n'
        self.indent += 1
        for stmt in node.list:
            text += getattr(self, _get_node_type(stmt))(stmt)
        self.indent -= 1
        text += '%s}\n' % (self.indent * INDENT)
        return text

    def selector_expr(self, node):
        text = '%s.%s' % (
            getattr(self, _get_node_type(node.x))(node.x),
            getattr(self, _get_node_type(node.sel))(node.sel)
        )
        return text

    def call_expr(self, node):
        text = '%s(' % getattr(self, _get_node_type(node.fun))(node.fun)
        for arg in node.args:
            text += '%s, ' % getattr(self, _get_node_type(arg))(arg)
        if node.args:
            text = text[:-2]
        if node.ellipsis and len(node.args) == 1:
            text += '...'
        text += ')'
        return text

    def value_spec(self, node):
        text = ''
        for name in node.names:
            text += '%s, ' % name
        if node.names:
            text = text[:-2]
        if node.type is not None:
            text += ' %s' % getattr(self, _get_node_type(node.type))(node.type)
        if node.values:
            text += ' = '
        for value in node.values:
            text += '%s, ' % getattr(self, _get_node_type(value))(value)
        if node.values:
            text = text[:-2]
        return text

    def comment(self, node):
        return '// %s' % node.text

    def str(self, node):
        return node

    def expr_stmt(self, node):
        return '%s%s\n' % (
            self.indent * INDENT,
            getattr(self, _get_node_type(node.expr))(node.expr)
        )

    def assign_stmt(self, node):
        disable_lhs = True
        if isinstance(node.lhs, list):
            for _node in node.lhs:
                if isinstance(_node, Ident) and _node.name == '_':
                    continue
                else:
                    disable_lhs = False
        else:
            disable_lhs = False
            if isinstance(node.lhs, Ident) and node.lhs.name == '_':
                disable_lhs = True

        if disable_lhs:
            return '%s%s\n' % (
                self.indent * INDENT,
                getattr(self, _get_node_type(node.rhs))(node.rhs),
            )
        else:
            return '%s%s %s %s\n' % (
                self.indent * INDENT,
                getattr(self, _get_node_type(node.lhs))(node.lhs),
                node.token,
                getattr(self, _get_node_type(node.rhs))(node.rhs),
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
        p1 = x if node.right else node.op
        p2 = node.op if node.right else x
        return '%s%s' % (
            p1,
            p2
        )

    def paren_expr(self, node):
        x = node.x
        x = getattr(self, _get_node_type(x))(x) if not isinstance(x, str) else x
        return '(%s)' % x

    def list(self, node, separator=', ', indent=''):
        text = ''
        for elt in node:
            text += '%s%s%s' % (
                indent,
                getattr(self, _get_node_type(elt))(elt),
                separator
            )
        if node and not indent:
            text = text[:-2]
        return text

    def for_stmt(self, node):
        text = '%sfor ' % (self.indent * INDENT)
        if node.init is not None:
            text += '%s; ' % getattr(self, _get_node_type(node.init))(node.init).lstrip().rstrip()
            text += '%s; ' % getattr(self, _get_node_type(node.cond))(node.cond)
            text += '%s ' % getattr(self, _get_node_type(node.post))(node.post).lstrip().rstrip()
        elif node.cond is not None:
            text += '%s ' % getattr(self, _get_node_type(node.cond))(node.cond)
        text += getattr(self, _get_node_type(node.body))(node.body)
        return text

    def range_stmt(self, node):
        text = '%sfor' % (self.indent * INDENT)
        if node.key is not None:
            text += ' %s' % getattr(self, _get_node_type(node.key))(node.key).lstrip().rstrip()
        if node.value is not None:
            text += ', %s' % getattr(self, _get_node_type(node.value))(node.value).lstrip().rstrip()
        text += '%s range %s %s' % (
            (' %s' % node.tok) if node.tok != Token.ILLEGAL else '',
            getattr(self, _get_node_type(node.x))(node.x).lstrip().rstrip(),
            getattr(self, _get_node_type(node.body))(node.body)
        )
        return text

    def branch_stmt(self, node):
        text = '%s%s' % (
            self.indent * INDENT,
            node.tok
        )
        if node.label is not None:
            text += ' %s' % (node.label)
        text += '\n'
        return text

    def labeled_stmt(self, node):
        return '%s%s:\n' % (
            self.indent * INDENT,
            node.label
        )

    def if_stmt(self, node):
        text = '%sif ' % (self.indent * INDENT)
        if node.init is not None:
            text += '%s; ' % getattr(self, _get_node_type(node.init))(node.init).lstrip().rstrip()
        text += '%s ' % getattr(self, _get_node_type(node.cond))(node.cond)
        text += getattr(self, _get_node_type(node.body))(node.body)
        if node._else is not None:
            text = text.rstrip()
            text += ' else %s' % getattr(self, _get_node_type(node._else))(node._else).lstrip()
        return text

    def switch_stmt(self, node):
        text = '%sswitch ' % (self.indent * INDENT)
        if node.init is not None:
            text += '%s ' % getattr(self, _get_node_type(node.init))(node.init).lstrip().rstrip()
        if node.tag is not None:
            if node.init is not None:
                text = '%s; ' % text.rstrip()
            text += '%s ' % getattr(self, _get_node_type(node.tag))(node.tag)
        text += getattr(self, _get_node_type(node.body))(node.body)
        return text

    def case_clause(self, node):
        keyword = 'case ' if node.list else 'default'
        text = '%s%s' % (
            (self.indent - 1) * INDENT,
            keyword
        )
        for elt in node.list:
            text += '%s, ' % getattr(self, _get_node_type(elt))(elt)
        if node.list:
            text = text[:-2]
        text += ':\n'
        for elt in node.body:
            text += getattr(self, _get_node_type(elt))(elt)
        return text

    def array_type(self, node):
        return '[%s]%s' % (
            getattr(self, _get_node_type(node.len))(node.len),
            getattr(self, _get_node_type(node.elt))(node.elt)
        )

    def index_expr(self, node):
        return '%s[%s]' % (
            getattr(self, _get_node_type(node.x))(node.x),
            getattr(self, _get_node_type(node.index))(node.index)
        )

    def basic_lit(self, node):
        if node.kind == Token.STRING:
            return '"%s"' % re.sub(r'(?<!\\)(?:\\{2})*\"', '\\"', str(node.value))
        elif node.kind == Token.CHAR:
            return '\'%s\'' % node.value
        elif node.kind == Token.TRUE:
            return 'true'
        elif node.kind == Token.FALSE:
            return 'false'
        else:
            return node.value

    def composite_lit(self, node):
        if node.elts:
            text = '%s{\n' % getattr(self, _get_node_type(node.type))(node.type)
            self.indent += 1
            text += '%s' % getattr(self, _get_node_type(node.elts))(
                node.elts,
                separator=',\n',
                indent=(self.indent * INDENT)
            )
            self.indent -= 1
            text += '%s}' % (self.indent * INDENT)
            return text
        else:
            return '%s{}' % getattr(self, _get_node_type(node.type))(node.type)

    def decl_stmt(self, node):
        return getattr(self, _get_node_type(node.decl))(node.decl)

    def gen_decl(self, node):
        text = '%s%s ' % (
            self.indent * INDENT,
            node.tok
        )
        if len(node.specs) > 1:
            text += '(\n'
            self.indent += 1
        for spec in node.specs:
            if len(node.specs) > 1:
                text += '%s%s\n' % (
                    self.indent * INDENT,
                    getattr(self, _get_node_type(spec))(spec).rstrip()
                )
            else:
                text += getattr(self, _get_node_type(spec))(spec)
        if len(node.specs) > 1:
            self.indent -= 1
            text += ')\n'
        return text + '\n'

    def ident(self, node):
        return node.name

    def type_assert_expr(self, node):
        _type = 'type' if node.type is None else getattr(self, _get_node_type(node.type))(node.type)
        return '%s.(%s)' % (
            getattr(self, _get_node_type(node.x))(node.x),
            _type
        )

    def slice_expr(self, node):
        low = node.low if node.low is not None else ''
        high = node.high if node.high is not None else ''
        text = '%s[%s:%s' % (
            getattr(self, _get_node_type(node.x))(node.x),
            getattr(self, _get_node_type(low))(low),
            getattr(self, _get_node_type(high))(high)
        )
        if node.slice3:
            _max = node.max if node.max is not None else ''
            text += ':%s' % getattr(self, _get_node_type(_max))(_max)
        return text + ']'

    def map_type(self, node):
        return 'map[%s]%s' % (
            getattr(self, _get_node_type(node.key))(node.key),
            getattr(self, _get_node_type(node.value))(node.value)
        )

    def key_value_expr(self, node):
        return '%s: %s' % (
            getattr(self, _get_node_type(node.key))(node.key),
            getattr(self, _get_node_type(node.value))(node.value)
        )

    def ellipsis(self, node):
        return '...%s' % getattr(self, _get_node_type(node.type))(node.type)

    def func_lit(self, node):
        return 'func%s %s' % (
            getattr(self, _get_node_type(node.type))(node.type),
            getattr(self, _get_node_type(node.body))(node.body).rstrip()
        )

    def star_expr(self, node):
        return '*%s' % getattr(self, _get_node_type(node.x))(node.x)

    def type_spec(self, node):
        return '%s %s' % (
            getattr(self, _get_node_type(node.name))(node.name),
            getattr(self, _get_node_type(node.type))(node.type)
        )

    def struct_type(self, node):
        return 'struct {\n%s\n}\n' % (
            getattr(self, _get_node_type(node.fields))(
                node.fields,
                separator='\n',
                indent=((self.indent + 1) * INDENT)
            )
        )

    def interface_type(self, node):
        text = 'interface'
        if node.methods.list:
            text += ' {\n%s\n}\n' % getattr(self, _get_node_type(node.methods))(
                node.methods,
                separator='\n',
                indent=((self.indent + 1) * INDENT)
            )
        else:
            text += '{}'
        return text


def unparse(tree):
    generator = Generator()
    if isinstance(tree, (tuple, list)):
        result = ''
        for elt in tree:
            result += getattr(generator, _get_node_type(elt))(elt).rstrip() + '\n'
        return result
    else:
        return getattr(generator, _get_node_type(tree))(tree).rstrip() + '\n'
