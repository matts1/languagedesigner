from ebnf.basenode import Node

DIGITS = '1234567890'


# group = '(', definition list, ')'
class Group(Node):
    def create(self):
        if not self.match('('):
            return

        # Infinite loop here
        from ebnf.definitionlist import DefinitionList  # import loop
        self.definition = DefinitionList(self, make_invalid=True)

        if not self.match(')'):
            raise SyntaxError('Unclosed brackets')
        self.min_repeats = 1
        self.max_repeats = 1

        if self.valid:
            next = self.get()
            if next is not None and next in '*+{?':
                self.next()

            if next == '?':
                self.min_repeats = 0
            if next == '*':
                self.min_repeats = 0
                self.max_repeats = float('inf')
            elif next == '+':
                self.min_repeats = 1
                self.max_repeats = float('inf')
            elif next == '{':
                comma = False
                if self.match(',', set_invalid=False):
                    self.min_repeats = 0
                    comma = True
                else:
                    num = ''
                    while self.get() is not None and self.get() in DIGITS:
                        num += self.get(move=True)
                    if not num:
                        raise SyntaxError('Repetitions was invalid')
                    self.min_repeats = int(num)

                    if self.match(',', set_invalid=False):
                        comma = True
                    else:
                        self.max_repeats = self.min_repeats

                if comma:
                    num = ''
                    while self.get() is not None and self.get() in DIGITS:
                        num += self.get(move=True)
                    if not num:
                        self.max_repeats = float('inf')
                    else:
                        self.max_repeats = int(num)
                if not self.match('}'):
                    raise SyntaxError('Unfinished repetitions')

    def out(self):
        return '%s-%s repeats%s' % (
            self.min_repeats,
            self.max_repeats
        )
