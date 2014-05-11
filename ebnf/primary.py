from ebnf.basenode import Node, InvisibleCompiled
from ebnf.group import Group
from ebnf.metaidentifier import MetaIdentifier
from ebnf.string import String

# primary = numbered sequence | grouped sequence | meta identifier
# | terminal string | empty;
class Primary(Node):
    compiled_class = InvisibleCompiled

    def create(self):
        # don't match empty - I think it could create inf loops
        classes = [Group, MetaIdentifier, String]  #, Empty]
        self.valid = False
        for cls in classes:
            if cls(self).valid:
                self.valid = True
                self.child = self.children[0]
                break  # match only the first valid one

    def pprint(self, *args, **kwargs):
        return self.children[0].pprint(*args, **kwargs)

class Except(Primary):
    pass


class Empty(Node):
    def create(self):
        pass
