from ebnf.basenode import Node, RuleError, Compiled
from ebnf.syntaxrule import SyntaxRule


# syntax = (syntax rule)+
class Syntax(Node):
    def create(self):
        self.rules = {}
        self.skip_ignore()  # in case there's whitespace at the start
        while not self.is_end():
            if not SyntaxRule(self).valid:
                raise RuleError('The E-NBF is not valid, starting from the syntax rule "%s"' % (self.get(50)))
        for child in self.children:
            self.rules[child.identifier.identifier] = child.dl

        if not self.children:
            raise RuleError('The E-BNF must contain at least 1 syntax rule')

        for rule in self.rules:
            self.rules[rule].check_invalid(rule)

    def __getitem__(self, item):
        return self.rules[item]

    def compile(self, *args, **kwargs):
        # first node is root node
        return self.children[0].dl.compile(*args, **kwargs)

    # TODO: ensure multiple definitions of a syntax rule become a single definition
    # containing each definition list

class Program(Compiled):
    def create(self):
        pass
