#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: __init__
    :synopsis: module that contains enums.
"""


from enum import Enum


class Token(Enum):
    ILLEGAL = 1
    EOF = 2
    COMMENT = 3
    IDENT = 4
    INT = 5
    FLOAT = 6
    IMAG = 7
    CHAR = 8
    STRING = 9
    ADD = 10
    SUB = 11
    MUL = 12
    QUO = 13
    REM = 14
    AND = 15
    OR = 16
    XOR = 17
    SHL = 18
    SHR = 19
    AND_NOT = 20
    AND_ASSIGN = 21
    OR_ASSIGN = 22
    XOR_ASSIGN = 23
    SHL_ASSIGN = 24
    SHR_ASSIGN = 25
    AND_NOT_ASSIGN = 26
    LAND = 27
    LOR = 28
    ARROW = 29
    INC = 30
    DEC = 31
    EQL = 32
    LSS = 33
    GTR = 34
    ASSIGN = 35
    NOT = 36
    NEQ = 37
    LEQ = 38
    GEQ = 39
    DEFINE = 40
    ELLIPSIS = 41
    LPAREN = 42
    LBRACK = 43
    LBRACE = 44
    COMMA = 45
    PERIOD = 46
    RPAREN = 47
    RBRACK = 48
    RBRACE = 49
    SEMICOLON = 50
    COLON = 51
    BREAK = 52
    CASE = 53
    CHAN = 54
    CONST = 55
    CONTINUE = 56
    DEFAULT = 57
    DEFER = 58
    ELSE = 59
    FALLTHROUGH = 60
    FOR = 61
    FUNC = 62
    GO = 63
    GOTO = 64
    IF = 65
    IMPORT = 66
    INTERFACE = 67
    MAP = 68
    PACKAGE = 69
    RANGE = 70
    RETURN = 71
    SELECT = 72
    STRUCT = 73
    SWITCH = 74
    TYPE = 75
    VAR = 76
    TRUE = 77
    FALSE = 78
