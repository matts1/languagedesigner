from ebnf import TextNode, ExecuteNode

class Variable(TextNode):
    identifier = 'variable'
    def execute(self):
        try:
            return self.state.vars[self.val]
        except KeyError as E:
            raise NameError('Variable %s is not defined. Variables are %r' % (self.val, self.state.vars))

    def set(self, value):
        self.state.vars[self.val] = value

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
        fns = {'print': self.output, 'input': self.input, 'int': int, 'str': str, 'float': float}
        return fns[results[0]](*results[1:])

class Assignment(ExecuteNode):
    identifier = 'assignment'
    def execute(self):
        self.meta_children[0].set(self.meta_children[1].execute())

class Conditional(ExecuteNode):
    identifier = 'conditional'
    def execute(self):
        if self.meta_child.execute():
            self.meta_children[1].execute()

class Loop(ExecuteNode):
    identifier = 'loop'
    def execute(self):
        while self.meta_child.execute():
            self.meta_children[1].execute()

class State(object):
    def __init__(self):
        self.vars = {}
