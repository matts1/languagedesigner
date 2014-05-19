from ebnf import ExecuteNode, TextNode


class Expression(ExecuteNode):
    identifier = 'expression'
    def execute(self):
        if self.child.selected == 0:  # number
            return self.meta_children[0].val
        else:
            results = self.execute_children()
            result = eval('%r %s %r' % tuple(results))
            if self.is_root:
                self.output(result)
            return result


class Number(TextNode):
    identifier = 'number'
    def setup(self):
        self.val = eval(self.get_text())


class Operator(TextNode):
    identifier = 'operator'

bob = 'blah'  # testing that it doesn't try and import this
