from ebnf.basenode import Node
from ebnf.definitionlist import DefinitionList
from ebnf.metaidentifier import MetaIdentifier


# syntax rule = meta identifier, '=', definition list, ';'
class SyntaxRule(Node):
    def create(self):
        self.identifier = MetaIdentifier(self)
        self.match('=')
        self.dl = DefinitionList(self)
        self.match(';')

    def out(self):
        return self.identifier.identifier

    def children_out(self):
        return self.dl.children
