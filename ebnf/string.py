from ebnf.basenode import Node

class String(Node):
    ignore = set()

    def create(self):
        first = self.get(True)
        if first is None or first not in '"\'':
            self.valid = False
            return
        start = self.upto
        while self.get() not in (first, None):
            self.next()

        if self.get() is None:
            raise SyntaxError('String was not closed')
        self.val = self.text[start:self.upto]
        self.next()  # get past the closing of the string

    def out(self):
        return self.val
