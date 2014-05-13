from ebnf.basenode import Node, Compiled
from ebnf.singledefinition import SingleDefinition


class CompiledDefinitionList(Compiled):
    def create(self):
        for i, child in enumerate(self.ebnf.children):
            # only valid if one of its children is valid
            if child.compile(self, make_invalid=False).valid:
                self.selected_child = i
                break
        if not self.children:
            self.valid = False

    def should_delete(self):
        return len(self.ebnf.children) == 1

    def out(self):
        return 'index=' + str(self.selected_child)


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

    def check_invalid(self, ident):
        for child in self.children:
            child.check_invalid(ident)

    def out(self):
        return 'options'
