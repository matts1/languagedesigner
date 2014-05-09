from ebnf.basenode import Node
from ebnf.singledefinition import SingleDefinition


# definition list = single definition, ('|', single definition)*
class DefinitionList(Node):
    def create(self):
        SingleDefinition(self, make_invalid=True)
        while self.get() == '|':
            self.next()
            SingleDefinition(self, make_invalid=True)

    def pprint(self, indent=0):
        if len(self.children) == 1:
            return self.children[0].pprint(indent)
        else:
            return super(DefinitionList, self).pprint(indent)

    def out(self):
        return 'options'
