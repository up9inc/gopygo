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
        return text

    def _import(self, node):
        text = 'import %s\n' % node.path
        return text

    def func_decl(self, node):
        text = 'func %s(' % node.name
        for param in node.params:
            pass  # TODO ?
        text += ') {\n'
        self.indent += 1
        text += getattr(self, _get_node_type(node.body))(node.body)
        self.indent -= 1
        text += '}\n'
        return text

    def selector_expr(self, node):
        text = '%s%s.%s\n' % (
            self.indent * INDENT,
            node.x,
            getattr(self, _get_node_type(node.sel))(node.sel)
        )
        return text

    def call_expr(self, node):
        text = '%s(' % node.fun
        for arg in node.args:
            text += '%s, ' % getattr(self, _get_node_type(arg))(arg)
        text = text[:-2]
        text += ')'
        return text

    def value_spec(self, node):
        text = node.value
        if node._type:
            pass  # TODO ?
        return text

    def comment(self, node):
        return '// %s\n' % node.text


def unparse(tree):
    generator = Generator()
    return getattr(generator, _get_node_type(tree))(tree)
