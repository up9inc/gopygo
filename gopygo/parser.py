#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: __init__
    :synopsis: Go parser module.
"""

from sly import Lexer, Parser

from gopygo.ast import (
    Package,
    ImportSpec,
    FuncDecl,
    FuncType,
    FieldList,
    Field,
    BlockStmt,
    SelectorExpr,
    CallExpr,
    ValueSpec,
    Comment,
    Stmt,
    AssignStmt,
    ReturnStmt,
    BinaryExpr,
    UnaryExpr,
    ParenExpr
)
from gopygo.exceptions import (
    LexerError
)


def flatten(p):
    new = []
    for i in p:
        if isinstance(i, tuple):
            new += i
        else:
            new.append(i)
    return tuple(new)


class GoLexer(Lexer):
    tokens = {
        # Keywords
        PACKAGE, IMPORT, FUNC, RETURN, VAR,

        # Data types
        BOOL,
        INT8, INT16, INT32, INT64,
        UINT8, UINT16, UINT32, UINT64,
        INT, UINT, RUNE, BYTE, UINTPTR,
        FLOAT32, FLOAT64,
        COMPLEX64, COMPLEX128,
        STRING,

        # Literals
        NAME, NUMBER, STRING_LITERAL, TRUE, FALSE,

        # Comment
        COMMENT,

        # Operators
        ASSIGN, DEFINE,
        PLUS, TIMES, MINUS, DIVIDE,
        LPAREN, RPAREN, LBRACE, RBRACE,

        # Separators
        DOT, NEWLINE, COMMA
    }

    ignore = ' \t'

    # Keywords
    PACKAGE = 'package'
    IMPORT = 'import'
    FUNC = 'func'
    RETURN = 'return'
    VAR = 'var'

    # Data types
    BOOL = 'bool'
    INT8 = 'int8'
    INT16 = 'int16'
    INT32 = 'int32'
    INT64 = 'int64'
    UINT8 = 'uint8'
    UINT16 = 'uint16'
    UINT32 = 'uint32'
    UINT64 = 'uint64'
    INT = 'int'
    UINT = 'uint'
    RUNE = 'rune'
    BYTE = 'byte'
    UINTPTR = 'uintptr'
    FLOAT32 = 'float32'
    FLOAT64 = 'float64'
    COMPLEX64 = 'complex64'
    COMPLEX128 = 'complex128'
    STRING = 'string'

    # Literals
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER = r'[0-9]+\.[0-9]+|[0-9]+'
    STRING_LITERAL = r'\"(\$\{.*\}|\\.|[^\"\\])*\"'

    # Comment
    COMMENT = r'//.*\n'

    # Operators
    ASSIGN = r'='
    DEFINE = r':='
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACE = r'{'
    RBRACE = r'}'

    # Separators
    DOT = r'\.'
    NEWLINE = r'\n'
    COMMA = r'\,'

    # # Ignored pattern
    # ignore_newline = r'\n+'

    # # Extra action for newlines
    # def ignore_newline(self, t):
    #     self.lineno += t.value.count('\n')

    def error(self, t):
        raise LexerError("Illegal character '%s'" % t.value[0])


class GoParser(Parser):
    tokens = GoLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        ('right', UMINUS),
    )

    def __init__(self):
        self.names = { }

    @_(
        'line'
    )
    def start(self, p):
        if isinstance(p.line, tuple) and len(p.line) == 1:
            return p.line[0]
        else:
            return p.line

    @_(
        'package NEWLINE line',
        'package NEWLINE',
        'NEWLINE line',
        '_import NEWLINE line',
        '_import NEWLINE',
        'comment line',
        'comment',
        'func NEWLINE line',
        'func NEWLINE',
        'stmt line',
        'stmt'
    )
    def line(self, p):
        if isinstance(p[0], Package):
            package = p[0]
            if len(p) > 2:
                for i in p.line:
                    if isinstance(i, ImportSpec):
                        package.imports.append(i)
                    else:
                        package.decls.append(i)
            return package
        else:
            if isinstance(p[0], Comment):
                p[0].text += '\n'
            if len(p) > 1:
                return tuple(filter(lambda x: x!= '\n', flatten(p)))
            else:
                return p[0]

    @_('PACKAGE NAME')
    def package(self, p):
        return Package(p.NAME)

    @_('IMPORT STRING_LITERAL')
    def _import(self, p):
        return ImportSpec(p.STRING_LITERAL)

    @_('FUNC NAME func_type block_stmt')
    def func(self, p):
        return FuncDecl(p.NAME, p.func_type, p.block_stmt)

    @_(
        'LPAREN field_list RPAREN field_list',
        'LPAREN field_list RPAREN LPAREN field_list RPAREN'
    )
    def func_type(self, p):
        return FuncType(p.field_list0, p.field_list1)

    @_(
        '',
        'field',
        'field COMMA field_list'
    )
    def field_list(self, p):
        if len(p) > 2:
            return FieldList([p.field] + p.field_list.list)
        elif len(p) == 1:
            return FieldList([p.field])
        else:
            return FieldList([])

    @_(
        'STRING',
        'NAME STRING'
    )
    def field(self, p):
        if len(p) == 2:
            return Field(p.NAME, p[1])
        else:
            return Field(None, p[0])

    @_(
        'LBRACE stmts RBRACE',
        'LBRACE NEWLINE stmts RBRACE'
    )
    def block_stmt(self, p):
        return BlockStmt(p.stmts)

    @_(
        'stmt',
        'stmt stmts'
    )
    def stmts(self, p):
        if len(p) > 1:
            return [p.stmt] + p.stmts
        else:
            return [p.stmt]

    @_(
        'expr',
        'expr NEWLINE'
    )
    def stmt(self, p):
        return Stmt(p.expr)

    @_('COMMENT')
    def comment(self, p):
        return Comment(p.COMMENT[2:].lstrip().rstrip())

    @_('NAME DOT expr')
    def expr(self, p):
        return SelectorExpr(p.NAME, p.expr)

    @_('NAME LPAREN args RPAREN')
    def expr(self, p):
        return CallExpr(p.NAME, p.args)

    @_('comment')
    def expr(self, p):
        return p.comment

    @_('assign_stmt NEWLINE')
    def stmt(self, p):
        return p.assign_stmt

    @_(
        'expr DEFINE expr',
        'expr ASSIGN expr'
    )
    def assign_stmt(self, p):
        return AssignStmt(p.expr0, p[1], p.expr1)

    @_(
        'RETURN args NEWLINE'
    )
    def stmt(self, p):
        return ReturnStmt(p.args)

    @_('value_spec')
    def expr(self, p):
        return p.value_spec

    @_('value_spec NEWLINE')
    def stmt(self, p):
        return Stmt(p.value_spec)

    @_(
        '',
        'value_spec',
        'NAME',
        'expr',
        'value_spec COMMA args',
        'expr COMMA args',
        'NAME COMMA args'
    )
    def args(self, p):
        if len(p) > 2:
            return [p[0]] + p[2]
        elif len(p) == 1:
            return [p[0]]
        else:
            return []

    @_(
        'BOOL',
        'INT8',
        'INT16',
        'INT32',
        'INT64',
        'UINT8',
        'UINT16',
        'UINT32',
        'UINT64',
        'INT',
        'UINT',
        'RUNE',
        'BYTE',
        'UINTPTR',
        'FLOAT32',
        'FLOAT64',
        'COMPLEX64',
        'COMPLEX128',
        'STRING',
    )
    def type(self, p):
        return p[0]

    @_(
        'VAR NAME COMMA value_spec type',
        'VAR NAME COMMA value_spec',
        'NAME COMMA value_spec type',
        'NAME COMMA value_spec',
        'VAR NAME type',
        'VAR NAME',
        'NAME type',
        'NAME'
    )
    def value_spec(self, p):
        if hasattr(p, 'value_spec'):
            return ValueSpec([p.NAME] + p.value_spec.names, p.value_spec.type, [])
        elif len(p) > 1:
            _type = None
            if hasattr(p, 'type'):
                _type = p.type
            return ValueSpec([p.NAME], _type, [], is_decl=hasattr(p, 'VAR'))
        else:
            return ValueSpec([p.NAME], None, [])

    @_('expr PLUS expr')
    def expr(self, p):
        return BinaryExpr(p.expr0, '+', p.expr1)

    @_('expr MINUS expr')
    def expr(self, p):
        return BinaryExpr(p.expr0, '-', p.expr1)

    @_('expr TIMES expr')
    def expr(self, p):
        return BinaryExpr(p.expr0, '*', p.expr1)

    @_('expr DIVIDE expr')
    def expr(self, p):
        return BinaryExpr(p.expr0, '/', p.expr1)

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return UnaryExpr('-', p.expr)

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return ParenExpr(p.expr)

    @_('expr COMMA expr')
    def expr(self, p):
        return [p.expr0] + list(flatten(p.expr1))

    @_('STRING_LITERAL')
    def expr(self, p):
        return p.STRING_LITERAL

    @_('NUMBER')
    def expr(self, p):
        return p.NUMBER


lexer = GoLexer()
parser = GoParser()

def parse(text):
    return parser.parse(lexer.tokenize(text.lstrip()))
