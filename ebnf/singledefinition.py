from ebnf.basenode import Node
from ebnf.term import Term


# single definition = term, (',', term)*
class SingleDefinition(Node):
    def create(self):
        Term(self, make_invalid=True)
        while self.get() == ',':
            self.next()
            Term(self, make_invalid=True)

        if not self.valid:
            raise SyntaxError('Single definition was invalid')

    def pprint(self, indent=0):
        if len(self.children) == 1:
            return self.children[0].pprint(indent)
        else:
            return super(SingleDefinition, self).pprint(indent)

    def out(self):
        return 'sequence'
