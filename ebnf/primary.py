from ebnf.basenode import Node, Compiled
from ebnf.group import Group
from ebnf.metaidentifier import MetaIdentifier
from ebnf.string import String


class CompiledPrimary(Compiled):
    def create(self):
        self.ebnf.child.compile(self)


# primary = numbered sequence | grouped sequence | meta identifier
# | terminal string | empty;
class Primary(Node):
    compiled_class = CompiledPrimary

    def create(self):
        # don't match empty - I think it could create inf loops
        classes = [Group, MetaIdentifier, String]  #, Empty]
        self.valid = False
        for cls in classes:
            if cls(self).valid:
                self.valid = True
                self.child = self.children[0]
                break  # match only the first valid one

    def pprint(self, indent=0):
        return self.children[0].pprint(indent)

class Except(Primary):
    pass


class Empty(Node):
    def create(self):
        pass
