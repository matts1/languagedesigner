import re
from ebnf.basenode import Node, Compiled

identifier = re.compile('[a-z][a-z0-9 ]*', re.I)


class CompiledMetaIdentifier(Compiled):
    def create(self):
        self.ebnf.get_dl().compile(self, make_invalid=True)

    def out(self):
        return self.ebnf.identifier


# meta identifier = letter, (letter | decimal digit | ' ')*
class MetaIdentifier(Node):
    compiled_class = CompiledMetaIdentifier

    ignore = set('\f\n\r\t\v')
    def create(self):
        self.identifier = re.match(  # match goes from beginning of string only
            identifier,
            self.text[self.upto:]
        )
        if self.identifier is None:
            self.valid = False
        else:
            self.identifier = self.identifier.group(0).rstrip()
            self.next(len(self.identifier))

    def get_dl(self):
        return self.root[self.identifier]

    def out(self):
        return self.identifier
