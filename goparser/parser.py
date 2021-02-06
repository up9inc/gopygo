from sly import Lexer, Parser

from goparser.ast import (
    Package,
    ImportSpec,
    FuncDecl,
    SelectorExpr,
    CallExpr,
    ValueSpec,
    Comment
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
        PACKAGE, IMPORT, FUNC, NAME,
        COMMENT,
        NUMBER, STRING, PLUS,
        TIMES, MINUS, DIVIDE, ASSIGN,
        LPAREN, RPAREN, LBRACE, RBRACE,
        DOT, NEWLINE, COMMA
    }
    ignore = ' \t'

    # Keywords
    PACKAGE = 'package'
    IMPORT = 'import'
    FUNC = 'func'

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
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

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
                for i in p[2]:
                    print(i)
                    if i == '\n':
                        continue
                    elif isinstance(i, ImportSpec):
                        package.imports.append(i)
                    else:
                        package.decls.append(i)
            return package
        else:
            return flatten(p)

    @_('PACKAGE NAME')
    def package(self, p):
        return Package(p.NAME)

    @_('IMPORT STRING')
    def _import(self, p):
        return ImportSpec(p.STRING)

    @_('FUNC NAME LPAREN RPAREN LBRACE body RBRACE')
    def func(self, p):
        return FuncDecl('int', p.NAME, [], p.body)

    @_(
        'NEWLINE stmt' # Fill all cases
    )
    def body(self, p):
        return p[1]

    @_('COMMENT')
    def comment(self, p):
        return Comment(p.COMMENT[2:].lstrip().rstrip())

    @_('NAME DOT stmt')
    def stmt(self, p):
        return SelectorExpr(p.NAME, p.stmt)

    @_('NAME LPAREN call_params NEWLINE')
    def stmt(self, p):
        return CallExpr(p.NAME, p.call_params)

    @_('value RPAREN')
    def call_params(self, p):
        return [p.value]

    @_('STRING')
    def value(self, p):
        return ValueSpec('string', p.STRING)

    @_('NAME ASSIGN expr')
    def statement(self, p):
        self.names[p.NAME] = p.expr

    @_('expr')
    def statement(self, p):
        print(p.expr)

    @_('expr PLUS expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr MINUS expr')
    def expr(self, p):
        return p.expr0 - p.expr1

    @_('expr TIMES expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr DIVIDE expr')
    def expr(self, p):
        return p.expr0 / p.expr1

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return int(p.NUMBER)

    @_('NAME')
    def expr(self, p):
        try:
            return self.names[p.NAME]
        except LookupError:
            print(f'Undefined name {p.NAME!r}')
            return 0


lexer = GoLexer()
parser = GoParser()

def parse(text):
    return parser.parse(lexer.tokenize(text.lstrip()))
