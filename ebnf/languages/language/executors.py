from ebnf.eval import EvalNode, TextEvalNode

def my_print(*args):
    for arg in args:
        print arg,
    print

class Variable(TextEvalNode):
    identifier = 'variable'


class Builtin(TextEvalNode):
    identifier = 'builtin'


class Operator(TextEvalNode):
    identifier = 'operator'


class String(TextEvalNode):
    identifier = 'string'
    def setup(self):
        self.val = self.get_text()[1:-1]  # remove quotes


class Float(TextEvalNode):
    identifier = 'float'
    def setup(self):
        self.val = float(self.get_text())


class Int(TextEvalNode):
    identifier = 'integer'
    def setup(self):
        self.val = int(self.get_text())


class Bool(TextEvalNode):
    identifier = 'boolean'
    def setup(self):
        self.val = (self.get_text() == 'True')


class Expression(EvalNode):
    identifier = 'expression'
    def execute(self):
        if self.tree.selected < 6:  # number
            return self.execute_child(0)
        else:
            results = self.execute_children()
            result = eval('%r %s %r' % tuple(results))
            return result


class Function(EvalNode):
    identifier = 'function'
    def execute(self):
        results = self.execute_children()
        fns = {'print': my_print, 'input': raw_input, 'int': int, 'str': str, 'float': float}
        fns[results[0]](*results[1:])
