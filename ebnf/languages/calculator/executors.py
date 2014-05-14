from ebnf.eval import EvalNode

class Digit(EvalNode):
    identifier = 'digit'

    def setup(self):
        self.val = self.tree.child.val

    def execute(self):
        return self.val  # define this first

    def pprint(self):
        return self.val


class Expression(EvalNode):
    identifier = 'expression'

    def execute(self):
        if self.tree.selected == 0:  # number
            return self.meta_children[0].val
        else:
            results = self.execute_children()
            result = eval('%r %s %r' % tuple(results))
            if self.is_root:
                print result
            return result


class Number(EvalNode):
    identifier = 'number'

    def setup(self):
        self.val = int(''.join([c.val for c in self[0].children]))
        if len(self.children) > 1:  # floating point part too
            self.val += float('0.' + ''.join([c.val for c in self[1].meta_children]))

    def pprint(self):
        return self.val


class Operator(EvalNode):
    identifier = 'operator'

    def setup(self):
        self.op = self.tree.child.val

    def execute(self):
        return self.op

    def teardown(self):
        return

    def pprint(self):
        return self.op

bob = 'blah'  # testing that it doesn't try and import this
