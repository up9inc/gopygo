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

        # Identifiers and basic type literals
        IDENT, IMAG_LITERAL, FLOAT_LITERAL, INT_LITERAL, CHAR_LITERAL, STRING_LITERAL, TRUE, FALSE,

        # Comment
        COMMENT,

        # Operators
        ADD_ASSIGN, SUB_ASSIGN, MUL_ASSIGN, QUO_ASSIGN, REM_ASSIGN,
        AND_ASSIGN, OR_ASSIGN, XOR_ASSIGN, AND_NOT_ASSIGN, SHL_ASSIGN, SHR_ASSIGN,
        LAND, LOR, ARROW, INC, DEC, EQL, SHL, SHR, AND_NOT,
        NEQ, LEQ, GEQ, DEFINE, ELLIPSIS,
        ADD, SUB, MUL, QUO, REM, AND, OR, XOR, LSS, GTR, ASSIGN, NOT,

        # Delimiters
        LPAREN, LBRACK, LBRACE, COMMA, PERIOD,
        RPAREN, RBRACE, SEMICOLON, COLON,
        NEWLINE,
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

    # Identifiers and basic type literals
    IMAG_LITERAL = r'[0-9]+\.[0-9]+i|[0-9]+i'
    FLOAT_LITERAL = r'[0-9]+\.[0-9]+'
    INT_LITERAL = r'[0-9]+'
    CHAR_LITERAL = r'\'(\$\{.*\}|\\.|[^\'\\])*\''
    STRING_LITERAL = r'\"(\$\{.*\}|\\.|[^\"\\])*\"'
    TRUE = r'true'
    FALSE = r'false'
    IDENT = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # Comment
    COMMENT = r'//.*\n'

    # Operators
    ADD_ASSIGN = r'\+='
    SUB_ASSIGN = r'-='
    MUL_ASSIGN = r'\*='
    QUO_ASSIGN = r'/='
    REM_ASSIGN = r'%='
    AND_ASSIGN = r'&='
    OR_ASSIGN = r'\|='
    XOR_ASSIGN = r'\^='
    AND_NOT_ASSIGN = r'&\^='
    SHL_ASSIGN = r'<<='
    SHR_ASSIGN = r'>>='

    LAND = r'&&'
    LOR = r'\|\|'
    ARROW = r'<-'
    INC = r'\+\+'
    DEC = r'--'
    EQL = r'=='
    SHL = r'<<'
    SHR = r'>>'
    AND_NOT = r'&\^'
    NEQ = r'!='
    LEQ = r'<='
    GEQ = r'>='
    DEFINE = r':='
    ELLIPSIS = r'\.\.\.'

    ADD = r'\+'
    SUB = r'-'
    MUL = r'\*'
    QUO = r'/'
    REM = r'%'
    AND = r'&'
    OR = r'\|'
    XOR = r'\^'
    LSS = r'<'
    GTR = r'>'
    ASSIGN = r'='
    NOT = r'\!'

    # Delimiters
    LPAREN = r'\('
    LBRACK = r'\['
    LBRACE = r'{'
    COMMA = r'\,'
    PERIOD = r'\.'

    RPAREN = r'\)'
    RBRACE = r'}'
    SEMICOLON = r'\;'
    COLON = r'\:'

    NEWLINE = r'\n'

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
        ('left', ADD, SUB),
        ('left', MUL, QUO),
        ('right', USUB, UXOR, UNOT),
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

    @_('PACKAGE IDENT')
    def package(self, p):
        return Package(p.IDENT)

    @_('IMPORT STRING_LITERAL')
    def _import(self, p):
        return ImportSpec(p.STRING_LITERAL)

    @_('FUNC IDENT func_type block_stmt')
    def func(self, p):
        return FuncDecl(p.IDENT, p.func_type, p.block_stmt)

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
        'IDENT STRING'
    )
    def field(self, p):
        if len(p) == 2:
            return Field(p.IDENT, p[1])
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

    @_('IDENT PERIOD expr')
    def expr(self, p):
        return SelectorExpr(p.IDENT, p.expr)

    @_('IDENT LPAREN args RPAREN')
    def expr(self, p):
        return CallExpr(p.IDENT, p.args)

    @_('comment')
    def expr(self, p):
        return p.comment

    @_('assign_stmt NEWLINE')
    def stmt(self, p):
        return p.assign_stmt

    @_(
        'expr DEFINE expr',
        'expr ASSIGN expr',
        'expr ADD_ASSIGN expr',
        'expr SUB_ASSIGN expr',
        'expr MUL_ASSIGN expr',
        'expr QUO_ASSIGN expr',
        'expr REM_ASSIGN expr',
        'expr AND_ASSIGN expr',
        'expr OR_ASSIGN expr',
        'expr XOR_ASSIGN expr',
        'expr AND_NOT_ASSIGN expr',
        'expr SHL_ASSIGN expr',
        'expr SHR_ASSIGN expr',
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
        'IDENT',
        'expr',
        'value_spec COMMA args',
        'expr COMMA args',
        'IDENT COMMA args'
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
        'VAR IDENT COMMA value_spec type',
        'VAR IDENT COMMA value_spec',
        'IDENT COMMA value_spec type',
        'IDENT COMMA value_spec',
        'VAR IDENT type',
        'VAR IDENT',
        'IDENT type',
        'IDENT'
    )
    def value_spec(self, p):
        if hasattr(p, 'value_spec'):
            return ValueSpec([p.IDENT] + p.value_spec.names, p.value_spec.type, [])
        elif len(p) > 1:
            _type = None
            if hasattr(p, 'type'):
                _type = p.type
            return ValueSpec([p.IDENT], _type, [], is_decl=hasattr(p, 'VAR'))
        else:
            return ValueSpec([p.IDENT], None, [])

    @_(
        'expr LAND expr',
        'expr LOR expr',
        'expr ARROW expr',
        'expr EQL expr',
        'expr SHL expr',
        'expr SHR expr',
        'expr AND_NOT expr',
        'expr NEQ expr',
        'expr LEQ expr',
        'expr GEQ expr',
        'expr ADD expr',
        'expr SUB expr',
        'expr MUL expr',
        'expr QUO expr',
        'expr REM expr',
        'expr AND expr',
        'expr OR expr',
        'expr XOR expr',
        'expr LSS expr',
        'expr GTR expr'
    )
    def expr(self, p):
        return BinaryExpr(p.expr0, p[1], p.expr1)

    @_(
        'SUB expr %prec USUB',
        'XOR expr %prec UXOR',
        'NOT expr %prec UNOT',
    )
    def expr(self, p):
        return UnaryExpr(p[0], p.expr)

    @_(
        'INC expr',
        'expr INC',
        'DEC expr',
        'expr DEC'
    )
    def expr(self, p):
        op = p.INC if hasattr(p, 'INC') else p.DEC
        right = True if p[1] in ('++', '--') else False
        return UnaryExpr(op, p.expr, right=right)

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return ParenExpr(p.expr)

    @_('expr COMMA expr')
    def expr(self, p):
        return [p.expr0] + list(flatten(p.expr1))

    @_('IMAG_LITERAL')
    def expr(self, p):
        return p.IMAG_LITERAL

    @_('FLOAT_LITERAL')
    def expr(self, p):
        return p.FLOAT_LITERAL

    @_('INT_LITERAL')
    def expr(self, p):
        return p.INT_LITERAL

    @_('CHAR_LITERAL')
    def expr(self, p):
        return p.CHAR_LITERAL

    @_('STRING_LITERAL')
    def expr(self, p):
        return p.STRING_LITERAL

    @_('TRUE')
    def expr(self, p):
        return p.TRUE

    @_('FALSE')
    def expr(self, p):
        return p.FALSE


lexer = GoLexer()
parser = GoParser()

def parse(text):
    return parser.parse(lexer.tokenize(text.lstrip()))
