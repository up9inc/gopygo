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
        PACKAGE, IMPORT, FUNC, RETURN, VAR,
        T_STRING,
        NAME,
        COMMENT,
        NUMBER, STRING, PLUS,
        TIMES, MINUS, DIVIDE, ASSIGN, DEFINE,
        LPAREN, RPAREN, LBRACE, RBRACE,
        DOT, NEWLINE, COMMA
    }
    ignore = ' \t'

    # Keywords
    PACKAGE = 'package'
    IMPORT = 'import'
    FUNC = 'func'
    RETURN = 'return'
    VAR = 'var'
    T_STRING = 'string'

    # Tokens
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER = r'\d+'
    STRING = r'\"(\$\{.*\}|\\.|[^\"\\])*\"'

    COMMENT = r'//.*\n'

    # Special symbols
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    ASSIGN = r'='
    DEFINE = r':='
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACE = r'{'
    RBRACE = r'}'
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
        'package NEWLINE line',
        'package NEWLINE',
        'NEWLINE line',
        '_import NEWLINE line',
        '_import NEWLINE',
        'comment line',
        'comment',
        'func NEWLINE line',
        'func NEWLINE'
    )
    def line(self, p):
        if isinstance(p[0], Package):
            package = p[0]
            if len(p) > 2:
                for i in p.line:
                    if i == '\n':
                        continue
                    elif isinstance(i, ImportSpec):
                        package.imports.append(i)
                    else:
                        package.decls.append(i)
            return package
        else:
            if isinstance(p[0], Comment):
                p[0].text += '\n'
            return flatten(p)

    @_('PACKAGE NAME')
    def package(self, p):
        return Package(p.NAME)

    @_('IMPORT STRING')
    def _import(self, p):
        return ImportSpec(p.STRING)

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
        'T_STRING',
        'NAME T_STRING'
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

    @_('NAME')
    def expr(self, p):
        return p.NAME

    @_(
        'expr',
        'expr COMMA expr_list'
    )
    def expr_list(self, p):
        if len(p) > 1:
            return [p.expr] + p.expr_list
        else:
            return [p.expr]

    @_(
        'expr_list DEFINE expr_list',
        'expr_list ASSIGN expr_list'
    )
    def assign_stmt(self, p):
        return AssignStmt(p.expr_list0, p[1], p.expr_list1)

    @_(
        'RETURN args NEWLINE'
    )
    def stmt(self, p):
        return ReturnStmt(p.args)

    @_('value NEWLINE')
    def stmt(self, p):
        return Stmt(p.value)

    @_(
        '',
        'value',
        'NAME',
        'value COMMA args',
        'NAME COMMA args',
    )
    def args(self, p):
        if len(p) > 2:
            return [p[0]] + p[2]
        elif len(p) == 1:
            return [p[0]]
        else:
            return []

    @_(
        'STRING',
        'VAR NAME T_STRING'
    )
    def value(self, p):
        if len(p) > 2:
            return ValueSpec([p.NAME], p[2], [])
        else:
            return ValueSpec([], None, [p.STRING])

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

    @_('NUMBER')
    def expr(self, p):
        return p.NUMBER


lexer = GoLexer()
parser = GoParser()

def parse(text):
    return parser.parse(lexer.tokenize(text.lstrip()))
