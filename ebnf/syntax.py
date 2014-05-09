from ebnf.basenode import Node, RuleError
from ebnf.syntaxrule import SyntaxRule


# syntax = (syntax rule)+
class Syntax(Node):
    def create(self):
        self.skip_ignore()  # in case there's whitespace at the start
        while not self.is_end():
            if not SyntaxRule(self).valid:
                raise RuleError(
                'The E-NBF is not valid, starting from the syntax rule "%s"' % (self.get(50))
            )

        if not self.children:
            raise RuleError('The E-BNF must contain at least 1 syntax rule')

    # TODO: ensure multiple definitions of a syntax rule become a single definition
    # containing each definition list

