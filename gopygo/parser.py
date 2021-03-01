#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: __init__
    :synopsis: Go parser module.
"""

import os

from sly import Lexer, Parser
from sly.yacc import SlyLogger

from gopygo.ast import (
    Ident,
    BasicLit,
    CompositeLit,
    GenDecl,
    DeclStmt,
    Package,
    File,
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
    ExprStmt,
    AssignStmt,
    ReturnStmt,
    BinaryExpr,
    UnaryExpr,
    ParenExpr,
    ForStmt,
    BranchStmt,
    LabeledStmt,
    IfStmt,
    SwitchStmt,
    CaseClause,
    ArrayType,
    IndexExpr,
    TypeAssertExpr,
    SliceExpr,
    MapType,
    KeyValueExpr,
    RangeStmt,
    Ellipsis,
    FuncLit,
    StarExpr,
    StructType,
    TypeSpec,
    InterfaceType
)
from gopygo.exceptions import (
    LexerError
)
from gopygo.enums import Token


def flatten(p):
    new = []
    try:
        for i in p:
            if isinstance(i, tuple):
                new += i
            else:
                new.append(i)
    except TypeError:
        new.append(p)
    return tuple(new)


class GoLexer(Lexer):
    tokens = {
        # Keywords
        PACKAGE, FUNC, RETURN,
        IMPORT, VAR, CONST, TYPE,
        FOR, RANGE, BREAK, CONTINUE, GOTO, FALLTHROUGH,
        IF, ELSE,
        SWITCH, CASE, DEFAULT,
        MAP,
        STRUCT, INTERFACE,

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
        RPAREN, RBRACK, RBRACE, SEMICOLON, COLON,
        NEWLINE,
    }

    ignore = ' \t'

    # Keywords
    PACKAGE = 'package'
    FUNC = 'func'
    RETURN = 'return'
    IMPORT = 'import'
    VAR = 'var'
    CONST = 'const'
    TYPE = 'type'
    FOR = 'for'
    RANGE = 'range'
    BREAK = 'break'
    CONTINUE = 'continue'
    GOTO = 'goto'
    FALLTHROUGH = 'fallthrough'
    IF = 'if'
    ELSE = 'else'
    SWITCH = 'switch'
    CASE = 'case'
    DEFAULT = 'DEFAULT'
    MAP = 'map'
    STRUCT = 'struct'
    INTERFACE = 'interface'

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
    INT_LITERAL = r'[0-9]+e[0-9]+|[0-9]+'
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
    RBRACK = r'\]'
    RBRACE = r'}'
    SEMICOLON = r';'
    COLON = r':'

    NEWLINE = r'\n'

    # # Ignored pattern
    # ignore_newline = r'\n+'

    # # Extra action for newlines
    # def ignore_newline(self, t):
    #     self.lineno += t.value.count('\n')

    def error(self, t):
        raise LexerError("Illegal character '%s'" % t.value[0])


class GoParser(Parser):
    log = SlyLogger(open(os.devnull, 'w'))  # To enable logging: SlyLogger(sys.stderr)

    tokens = GoLexer.tokens

    precedence = (
        ('left', ADD, SUB),
        ('left', MUL, QUO),
        ('right', USUB, UXOR, UNOT, UADD),
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
        'func_decl NEWLINE line',
        'func_decl NEWLINE',
        'stmt line',
        'stmt'
    )
    def line(self, p):
        if isinstance(p[0], Package):
            file = File(p[0])
            if len(p) > 2:
                for i in p.line:
                    file.decls.append(i)
            return file
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

    @_(
        'IMPORT STRING_LITERAL',
        'IMPORT IDENT STRING_LITERAL',
        'IMPORT PERIOD STRING_LITERAL',
        'IMPORT LPAREN _import_list NEWLINE RPAREN',
        'IMPORT LPAREN _import_list RPAREN',
        'IMPORT LPAREN NEWLINE _import_list NEWLINE RPAREN',
        'IMPORT LPAREN NEWLINE _import_list RPAREN',
    )
    def _import(self, p):
        if hasattr(p, 'STRING_LITERAL'):
            ident = None
            if hasattr(p, 'IDENT'):
                ident = p.IDENT
            elif hasattr(p, 'PERIOD'):
                ident = p.PERIOD

            return GenDecl(
                p[0],
                [ImportSpec(ident, BasicLit(Token.STRING, p.STRING_LITERAL[1:-1]))]
            )
        else:
            return GenDecl(
                p[0],
                p._import_list
            )

    @_(
        'STRING_LITERAL',
        'STRING_LITERAL NEWLINE',
        'STRING_LITERAL _import_list',
        'STRING_LITERAL NEWLINE _import_list',
        'IDENT STRING_LITERAL',
        'IDENT STRING_LITERAL NEWLINE',
        'IDENT STRING_LITERAL _import_list',
        'IDENT STRING_LITERAL NEWLINE _import_list',
        'PERIOD STRING_LITERAL',
        'PERIOD STRING_LITERAL NEWLINE',
        'PERIOD STRING_LITERAL _import_list',
        'PERIOD STRING_LITERAL NEWLINE _import_list'
    )
    def _import_list(self, p):
        ident = None
        if hasattr(p, 'IDENT'):
            ident = p.IDENT
        elif hasattr(p, 'PERIOD'):
            ident = p.PERIOD

        if hasattr(p, '_import_list'):
            return [ImportSpec(ident, BasicLit(Token.STRING, p.STRING_LITERAL[1:-1]))] + p._import_list
        else:
            return [ImportSpec(ident, BasicLit(Token.STRING, p.STRING_LITERAL[1:-1]))]

    @_('FUNC IDENT func_type block_stmt')
    def func_decl(self, p):
        return FuncDecl(p.IDENT, p.func_type, p.block_stmt)

    @_('FUNC func_type block_stmt')
    def func_lit(self, p):
        return FuncLit(p.func_type, p.block_stmt)

    @_(
        'func_lit',
        'func_lit COMMA func_lits',
    )
    def func_lits(self, p):
        if hasattr(p, 'func_lits'):
            return [p.func_lit] + p.func_lits
        else:
            return [p.func_lit]

    @_(
        'LPAREN field_list RPAREN field_list',
        'LPAREN field_list RPAREN LPAREN field_list RPAREN'
    )
    def func_type(self, p):
        return FuncType(p.field_list0, p.field_list1)

    @_(
        '',
        'field',
        'field COMMA field_list',
        'field NEWLINE field_list'
    )
    def field_list(self, p):
        if len(p) > 2:
            return FieldList([p.field] + p.field_list.list)
        elif len(p) == 1:
            return FieldList([p.field])
        else:
            return FieldList([])

    @_(
        '_type',
        'ELLIPSIS _type',
        'IDENT _type',
        'IDENT ELLIPSIS _type',
        'FUNC LPAREN RPAREN _type',
        'FUNC LPAREN RPAREN ELLIPSIS _type',
        'IDENT LPAREN RPAREN _type',
        'IDENT LPAREN RPAREN ELLIPSIS _type',
        'MUL _type',
        'ELLIPSIS MUL _type',
        'IDENT MUL _type',
        'IDENT ELLIPSIS MUL _type',
        'FUNC LPAREN RPAREN MUL _type',
        'FUNC LPAREN RPAREN ELLIPSIS MUL _type',
        'IDENT LPAREN RPAREN MUL _type',
        'IDENT LPAREN RPAREN ELLIPSIS MUL _type',
        'MUL expr',
        'ELLIPSIS MUL expr',
        'IDENT MUL expr',
        'IDENT ELLIPSIS MUL expr',
        'FUNC LPAREN RPAREN MUL expr',
        'FUNC LPAREN RPAREN ELLIPSIS MUL expr',
        'IDENT LPAREN RPAREN MUL expr',
        'IDENT LPAREN RPAREN ELLIPSIS MUL expr',
    )
    def field(self, p):
        _type = None
        if not hasattr(p, '_type'):
            _type = StarExpr(p.expr)
        else:
            _type = StarExpr(p._type) if hasattr(p, 'MUL') else p._type

        if hasattr(p, 'LPAREN'):
            name = None
            if hasattr(p, 'IDENT'):
                name = p.IDENT
            return Field(
                name,
                FuncType(
                    FieldList([]),
                    FieldList([
                        Field(None, _type)
                    ])
                )
            )

        if hasattr(p, 'ELLIPSIS'):
            _type = Ellipsis(_type)

        if (hasattr(p, '_type') or hasattr(p, 'expr')) and hasattr(p, 'IDENT'):
            return Field(p.IDENT, _type)
        else:
            return Field(None, _type)

    @_(
        'LBRACE stmts RBRACE',
        'LBRACE NEWLINE stmts RBRACE',
        'LBRACE case_clause_list RBRACE',
        'LBRACE NEWLINE case_clause_list RBRACE',
    )
    def block_stmt(self, p):
        if hasattr(p, 'stmts'):
            return BlockStmt(p.stmts)
        elif hasattr(p, 'case_clause_list'):
            return BlockStmt(p.case_clause_list)

    @_(
        'case_clause',
        'case_clause case_clause_list',
    )
    def case_clause_list(self, p):
        if len(p) > 1:
            return [p.case_clause] + p.case_clause_list
        else:
            return [p.case_clause]

    @_(
        'stmt',
        'stmt stmts',
        'NEWLINE stmts'
    )
    def stmts(self, p):
        if p[0] == '\n':
            return p.stmts
        elif len(p) > 1:
            if isinstance(p.stmt, LabeledStmt) and p.stmt.label == 'default':
                return [CaseClause([], p.stmts)]
            return [p.stmt] + p.stmts
        else:
            return [p.stmt]

    @_(
        'expr',
        'expr NEWLINE'
    )
    def stmt(self, p):
        return ExprStmt(p.expr)

    @_('COMMENT')
    def comment(self, p):
        return Comment(p.COMMENT[2:].lstrip().rstrip())

    @_('call_expr')
    def expr(self, p):
        return p.call_expr

    @_(
        'selector_expr LPAREN args RPAREN',
        'IDENT LPAREN args RPAREN',
        '_type LPAREN args RPAREN',
        'selector_expr LPAREN args ELLIPSIS RPAREN',
        'IDENT LPAREN args ELLIPSIS RPAREN',
        '_type LPAREN args ELLIPSIS RPAREN',
    )
    def call_expr(self, p):
        ellipsis = True if hasattr(p, 'ELLIPSIS') else False
        return CallExpr(p[0], p.args, ellipsis=ellipsis)

    @_('selector_expr')
    def expr(self, p):
        return p.selector_expr

    @_(
        'IDENT PERIOD IDENT',
        'selector_expr PERIOD IDENT',
        'call_expr PERIOD IDENT'
    )
    def selector_expr(self, p):
        return SelectorExpr(p[0], p[2])

    @_(
        'IDENT PERIOD LPAREN expr RPAREN',
        'IDENT PERIOD LPAREN TYPE RPAREN',
        'expr PERIOD LPAREN expr RPAREN',
        'expr PERIOD LPAREN TYPE RPAREN',
    )
    def expr(self, p):
        _type = p[3] if p[3] != GoLexer.TYPE else None
        return TypeAssertExpr(p[0], p[3])

    @_('comment')
    def expr(self, p):
        return p.comment

    @_(
        'assign_stmt NEWLINE',
        'assign_stmt'
    )
    def stmt(self, p):
        return p.assign_stmt

    @_('for_stmt NEWLINE')
    def stmt(self, p):
        return p.for_stmt

    @_('range_stmt NEWLINE')
    def stmt(self, p):
        return p.range_stmt

    @_('if_stmt NEWLINE')
    def stmt(self, p):
        return p.if_stmt

    @_('switch_stmt NEWLINE')
    def stmt(self, p):
        return p.switch_stmt

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
        'FOR block_stmt',
        'FOR expr block_stmt',
        'FOR stmt SEMICOLON expr SEMICOLON stmt block_stmt'
    )
    def for_stmt(self, p):
        if len(p) == 2:
            return ForStmt(p.block_stmt)
        elif len(p) == 3:
            return ForStmt(p.block_stmt, cond=p.expr)
        else:
            return ForStmt(p.block_stmt, init=p.stmt0, cond=p.expr, post=p.stmt1)

    @_(
        'FOR RANGE expr block_stmt',
        'FOR expr DEFINE RANGE expr block_stmt',
        'FOR expr COMMA expr DEFINE RANGE expr block_stmt',
        'FOR expr ASSIGN RANGE expr block_stmt',
        'FOR expr COMMA expr ASSIGN RANGE expr block_stmt',
    )
    def range_stmt(self, p):
        tok = Token.ILLEGAL
        if hasattr(p, 'DEFINE'):
            tok = p.DEFINE
        elif hasattr(p, 'ASSIGN'):
            tok = p.ASSIGN

        if tok == Token.ILLEGAL:
            return RangeStmt(None, None, tok, p.expr, p.block_stmt)

        if hasattr(p, 'COMMA'):
            return RangeStmt(p.expr0, p.expr1, tok, p.expr2, p.block_stmt)
        else:
            return RangeStmt(p.expr0, None, tok, p.expr1, p.block_stmt)

    @_(
        'IF expr block_stmt',
        'IF expr block_stmt ELSE block_stmt',
        'IF expr block_stmt ELSE if_stmt',
        'IF stmt SEMICOLON expr block_stmt',
        'IF stmt SEMICOLON expr block_stmt ELSE block_stmt',
        'IF stmt SEMICOLON expr block_stmt ELSE if_stmt'
    )
    def if_stmt(self, p):
        init = p.stmt if hasattr(p, 'stmt') else None
        cond = p.expr
        body = p.block_stmt0 if hasattr(p, 'block_stmt0') else p.block_stmt
        _else = p[-1] if hasattr(p, 'ELSE') else None
        return IfStmt(
            cond,
            body,
            init=init,
            _else=_else
        )

    @_(
        'SWITCH block_stmt',
        'SWITCH stmt block_stmt',
        'SWITCH expr block_stmt',
        'SWITCH stmt SEMICOLON expr block_stmt'
    )
    def switch_stmt(self, p):
        init = p.stmt if hasattr(p, 'stmt') else None
        tag = p.expr if hasattr(p, 'expr') else None
        return SwitchStmt(
            p.block_stmt,
            init=init,
            tag=tag
        )

    @_(
        'CASE expr COLON NEWLINE stmts',
        'CASE _type_list COLON NEWLINE stmts',
        'DEFAULT COLON NEWLINE stmts',
    )
    def case_clause(self, p):
        expr = p.expr if hasattr(p, 'expr') else []
        _type_list = p._type_list if hasattr(p, '_type_list') else []
        expr = [expr] if not isinstance(expr, list) else expr
        _type_list = [_type_list] if not isinstance(_type_list, list) else _type_list
        expr += _type_list
        return CaseClause(expr, p.stmts)

    @_(
        '_type',
        '_type COMMA _type_list',
    )
    def _type_list(self, p):
        if len(p) > 1:
            return [p._type] + p._type_list
        else:
            return [p._type]

    @_(
        'RETURN args NEWLINE',
        'RETURN func_lits NEWLINE'
    )
    def stmt(self, p):
        return ReturnStmt(p[1])

    @_(
        'TYPE IDENT STRUCT LBRACE field_list RBRACE NEWLINE',
        'TYPE IDENT STRUCT LBRACE NEWLINE field_list RBRACE NEWLINE',
        'TYPE IDENT STRUCT LBRACE field_list NEWLINE RBRACE NEWLINE',
        'TYPE IDENT STRUCT LBRACE NEWLINE field_list NEWLINE RBRACE NEWLINE',
        'TYPE IDENT INTERFACE LBRACE field_list RBRACE NEWLINE',
        'TYPE IDENT INTERFACE LBRACE NEWLINE field_list RBRACE NEWLINE',
        'TYPE IDENT INTERFACE LBRACE field_list NEWLINE RBRACE NEWLINE',
        'TYPE IDENT INTERFACE LBRACE NEWLINE field_list NEWLINE RBRACE NEWLINE',
        'VAR value_spec NEWLINE',
        'CONST value_spec NEWLINE',
        'IMPORT value_spec NEWLINE',
        'TYPE value_spec NEWLINE',
    )
    def stmt(self, p):
        if hasattr(p, 'IDENT'):
            _type = None
            if hasattr(p, 'INTERFACE'):
                _type = InterfaceType(p.field_list, False)
            else:
                _type = StructType(p.field_list, False)
            return DeclStmt(
                GenDecl(
                    p[0],
                    [
                        TypeSpec(
                            p.IDENT,
                            _type
                        )
                    ]
                )
            )
        else:
            return DeclStmt(
                GenDecl(
                    p[0],
                    [p.value_spec]
                )
            )

    @_(
        'BREAK NEWLINE',
        'CONTINUE NEWLINE',
        'GOTO IDENT NEWLINE',
        'FALLTHROUGH NEWLINE'
    )
    def stmt(self, p):
        if hasattr(p, 'GOTO'):
            return BranchStmt(p.GOTO, p.IDENT)
        else:
            return BranchStmt(p[0])

    @_(
        'IDENT COLON'
    )
    def stmt(self, p):
        return LabeledStmt(p.IDENT)

    @_(
        '',
        'expr',
        'TYPE',
        'expr COMMA args',
        'TYPE COMMA args',
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
    def _type(self, p):
        return p[0]

    @_(
        'IDENT COMMA value_spec array_type ASSIGN expr',
        'IDENT COMMA value_spec _type ASSIGN expr',
        'IDENT COMMA value_spec ASSIGN expr',
        'IDENT array_type ASSIGN expr',
        'IDENT _type ASSIGN expr',
        'IDENT ASSIGN expr',
        'IDENT COMMA value_spec array_type',
        'IDENT COMMA value_spec _type',
        'IDENT COMMA value_spec',
        'IDENT array_type',
        'IDENT _type',
    )
    def value_spec(self, p):
        values = []
        if hasattr(p, 'ASSIGN'):
            values = p.expr
        values = [values] if not isinstance(values, list) else values

        if hasattr(p, 'value_spec'):
            values += p.value_spec.values
            return ValueSpec([p.IDENT] + p.value_spec.names, p.value_spec.type, values)
        else:
            _type = None
            if hasattr(p, 'array_type'):
                _type = p.array_type
            elif hasattr(p, '_type'):
                _type = p._type
            return ValueSpec([p.IDENT], _type, values)

    @_(
        'LBRACK expr RBRACK _type',
        'LBRACK expr RBRACK array_type',
        'LBRACK RBRACK _type',
        'LBRACK RBRACK array_type',
    )
    def array_type(self, p):
        _len = p.expr if hasattr(p, 'expr') else ''
        return ArrayType(_len, p[-1])

    @_(
        'expr LBRACK expr RBRACK'
    )
    def expr(self, p):
        return IndexExpr(p.expr0, p.expr1)

    @_(
        'expr LBRACK COLON expr RBRACK',
        'expr LBRACK expr COLON RBRACK',
        'expr LBRACK expr COLON expr RBRACK',
        'expr LBRACK expr COLON expr COLON expr RBRACK'
    )
    def expr(self, p):
        if len(p) == 5:
            if p[2] == GoLexer.COLON:
                return SliceExpr(p.expr0, None, p.expr1, None, False)
            else:
                return SliceExpr(p.expr0, p.expr1, None, None, False)
        if hasattr(p, 'expr3'):
            return SliceExpr(p.expr0, p.expr1, p.expr2, p.expr3, True)
        else:
            return SliceExpr(p.expr0, p.expr1, p.expr2, None, False)

    @_('map_type')
    def expr(self, p):
        return p.map_type

    @_(
        'MAP LBRACK expr RBRACK expr',
        'MAP LBRACK _type RBRACK _type',
        'MAP LBRACK _type RBRACK interface_type',
    )
    def map_type(self, p):
        return MapType(p[2], p[4])

    @_(
        'INTERFACE LBRACE field_list RBRACE'
    )
    def interface_type(sef, p):
        return InterfaceType(p.field_list, False)

    @_(
        'expr COLON expr',
        'expr COLON expr COMMA NEWLINE',
        'expr COLON expr COMMA key_value_list',
        'expr COLON expr COMMA NEWLINE key_value_list',
    )
    def key_value_list(self, p):
        if hasattr(p, 'key_value_list'):
            return [KeyValueExpr(p.expr0, p.expr1)] + p.key_value_list
        else:
            return [KeyValueExpr(p.expr0, p.expr1)]

    @_(
        'map_type LBRACE key_value_list RBRACE',
        'map_type LBRACE NEWLINE key_value_list RBRACE',
        'map_type LBRACE RBRACE',
    )
    def expr(self, p):
        expr = []
        if hasattr(p, 'key_value_list'):
            expr = p.key_value_list if isinstance(p.key_value_list, list) else [p.key_value_list]
        return CompositeLit(p.map_type, expr, False)

    @_(
        'array_type LBRACE expr RBRACE',
        'array_type LBRACE NEWLINE expr RBRACE',
        'array_type LBRACE expr NEWLINE RBRACE',
        'array_type LBRACE NEWLINE expr NEWLINE RBRACE',
        'array_type LBRACE RBRACE',
    )
    def expr(self, p):
        expr = []
        if hasattr(p, 'expr'):
            expr = p.expr if isinstance(p.expr, list) else [p.expr]
        return CompositeLit(p.array_type, expr, False)

    @_(
        'array_type'
    )
    def expr(self, p):
        return p.array_type

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
        'AND expr %prec UADD',
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

    @_('IMAG_LITERAL')
    def expr(self, p):
        return BasicLit(Token.IMAG, p.IMAG_LITERAL)

    @_('FLOAT_LITERAL')
    def expr(self, p):
        return BasicLit(Token.FLOAT, p.FLOAT_LITERAL)

    @_('INT_LITERAL')
    def expr(self, p):
        return BasicLit(Token.INT, p.INT_LITERAL)

    @_('CHAR_LITERAL')
    def expr(self, p):
        return BasicLit(Token.CHAR, p.CHAR_LITERAL[1:-1])

    @_('STRING_LITERAL')
    def expr(self, p):
        return BasicLit(Token.STRING, p.STRING_LITERAL[1:-1])

    @_('TRUE')
    def expr(self, p):
        return BasicLit(Token.TRUE, None)

    @_('FALSE')
    def expr(self, p):
        return BasicLit(Token.FALSE, None)

    @_(
        'expr COMMA expr',
        'expr COMMA NEWLINE expr'
    )
    def expr(self, p):
        return [p.expr0] + list(flatten(p.expr1))

    @_(
        'expr COMMA',
        'expr COMMA NEWLINE'
    )
    def expr(self, p):
        return p.expr

    @_('MUL IDENT')
    def expr(self, p):
        return StarExpr(Ident(p.IDENT))

    @_('IDENT')
    def expr(self, p):
        return Ident(p.IDENT)


lexer = GoLexer()
parser = GoParser()

def parse(text):
    return parser.parse(lexer.tokenize(text.lstrip().rstrip() + '\n'))
