from ebnf.basenode import Node, InvisibleCompiled
from ebnf.primary import Primary, Except


class CompiledTerm(InvisibleCompiled):
    def create(self):
        if self.ebnf.exception is None or not self.ebnf.exception.compile(self).valid:
            self.ebnf.primary.compile(self, make_invalid=True)
        else:
            self.valid = False

# term = primary, ('-', exception)?
# but an exception is a primary
class Term(Node):
    compiled_class = CompiledTerm


    def create(self):
        self.primary = Primary(self, make_invalid=True)
        self.exception = None

        if self.get() == '-':
            self.next()
            self.exception = Except(self)  # a primary is an exception
            if not self.exception.valid:
                raise SyntaxError('Invalid exception to rule after "-"')

    def pprint(self, indent=0, children=True):
        if self.exception is None:
            return self.primary.pprint(indent, children)
        else:
            return '%s<%s> \n%s\n%sExcepting %s' % (
                ' ' * indent,
                self.__class__.__name__,
                self.primary.pprint(indent + 2) if children else '',
                ' ' * (indent + 2),
                self.exception.pprint(indent + 2).lstrip() if children else ''
            )
