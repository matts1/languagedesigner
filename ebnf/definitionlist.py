from ebnf.basenode import Node, InvisibleCompiled
from ebnf.singledefinition import SingleDefinition


class CompiledDefinitionList(InvisibleCompiled):
    def create(self):
        for i, child in enumerate(self.ebnf.children):
            # only valid if one of its children is valid
            if child.compile(self, make_invalid=False).valid:
                self.selected_child = i
                break
        if not self.children:
            self.valid = False


# definition list = single definition, ('|', single definition)*
class DefinitionList(Node):
    compiled_class = CompiledDefinitionList

    def create(self):
        SingleDefinition(self, make_invalid=True)
        while self.get() == '|':
            self.next()
            SingleDefinition(self, make_invalid=True)

    def pprint(self, *args, **kwargs):
        if len(self.children) == 1:
            return self.children[0].pprint(*args, **kwargs)
        else:
            return super(DefinitionList, self).pprint(*args, **kwargs)

    def out(self):
        return 'options'
