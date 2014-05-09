from ebnf.basenode import Node
from ebnf.primary import Primary, Except


# term = primary, ('-', exception)?
# but an exception is a primary
class Term(Node):
    def create(self):
        self.primary = Primary(self, make_invalid=True)
        self.exception = None

        if self.get() == '-':
            self.next()
            self.exception = Except(self)  # a primary is an exception
            if not self.exception.valid:
                raise SyntaxError('Invalid exception to rule after "-"')

    def pprint(self, indent=0):
        if self.exception is None:
            return self.primary.pprint(indent)
        else:
            return '%s<%s> \n%s\n%sExcepting %s' % (
                ' ' * indent,
                self.__class__.__name__,
                self.primary.pprint(indent + 2),
                ' ' * (indent + 2),
                self.exception.pprint(indent + 2).lstrip()
            )
