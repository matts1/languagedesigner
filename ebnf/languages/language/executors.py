from ebnf import TextNode, ExecuteNode

def my_print(*args):
    for arg in args:
        print arg,
    print

class Variable(TextNode):
    identifier = 'variable'


class Builtin(TextNode):
    identifier = 'builtin'


class Operator(TextNode):
    identifier = 'operator'


class String(TextNode):
    identifier = 'string'
    def setup(self):
        self.val = self.get_text()[1:-1]  # remove quotes


class Float(TextNode):
    identifier = 'float'
    def setup(self):
        self.val = float(self.get_text())


class Int(TextNode):
    identifier = 'integer'
    def setup(self):
        self.val = int(self.get_text())


class Bool(TextNode):
    identifier = 'boolean'
    def setup(self):
        self.val = (self.get_text() == 'True')


class Expression(ExecuteNode):
    identifier = 'expression'
    def execute(self):
        if self.child.selected < 6:  # number
            return self.meta_child.execute()
        else:
            results = self.execute_children()
            result = eval('%r %s %r' % tuple(results))
            return result


class Function(ExecuteNode):
    identifier = 'function'
    def execute(self):
        results = self.execute_children()
        fns = {'print': my_print, 'input': raw_input, 'int': int, 'str': str, 'float': float}
        fns[results[0]](*results[1:])
