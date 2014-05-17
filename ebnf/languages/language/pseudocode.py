from ebnf import ExecuteNode, TextNode

class Program(ExecuteNode):
    identifier = 'program'
    def execute(self, indent=0):
        val = '\n'.join(
            ' ' * indent + line for line in '\n'.join(self.execute_children()).split('\n')
        )
        if self.is_root:
            print val
        return val


class Line(ExecuteNode):
    identifier = 'line'
    def execute(self):
        return self.meta_child.execute()


class Assignment(ExecuteNode):
    identifier = 'assignment'
    def execute(self):
        return 'SET %s TO %s' % (
            self.meta_child.execute(), self.meta_children[1].execute()
        )

class Variable(TextNode):
    identifier = 'variable'


class Expression(TextNode):
    identifier = 'expression'
    def execute(self):
        if self.child.selected == 0: # function
            return self.meta_child.execute()
        elif self.child.selected == 6:
            return self.val[1:-1]
        else:
            return self.val


class Function(ExecuteNode):
    identifier = 'function'
    def execute(self):
        if self.meta_child.get_text() == 'print':
            return 'OUTPUT ' + ', '.join(self.execute_children()[1:])  # don't execute builtin
        return self.get_text()


class Conditional(ExecuteNode):
    identifier = 'conditional'
    data = 'IF %s THEN\n%s\nEND IF'
    def execute(self):
        return self.data % (
            self.meta_child.execute(),
            self.meta_children[1].execute(4)
        )


class Loop(Conditional):
    identifier = 'loop'
    data = 'WHILE %s\n%s\nEND WHILE'
