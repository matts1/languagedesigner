import re
from ebnf.syntax import Syntax


class Parser(object):
    def __init__(self, filename, root=Syntax):
        # should parse according to standards in ebnf_syntax.ebnf
        text = open(filename, "rU").read()
        # remove the comments
        text = re.sub('\n\\s*#[^\n]*', '', '\n' + text)
        self.tree = root(None, text)

    def load_program(self, filename):
        raise NotImplementedError

if __name__ == '__main__':
    ebnf = Parser('ebnf_syntax.ebnf').tree
    print ebnf
