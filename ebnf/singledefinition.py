from ebnf.basenode import Node, Compiled
from ebnf.term import Term


class CompiledSingleDefinition(Compiled):
    def should_delete(self):
        return len(self.children) == 1

    def out(self):
        return 'length=' + str(len(self.children))


# single definition = term, (',', term)*
class SingleDefinition(Node):
    compiled_class = CompiledSingleDefinition  # compiled just compiles all the children

    def create(self):
        Term(self, make_invalid=True)
        while self.get() == ',':
            self.next()
            Term(self, make_invalid=True)

        if not self.valid:
            raise SyntaxError('Single definition was invalid')

    def pprint(self, *args, **kwargs):
        if len(self.children) == 1:
            return self.children[0].pprint(*args, **kwargs)
        else:
            return super(SingleDefinition, self).pprint(*args, **kwargs)

    def out(self):
        return 'sequence'
