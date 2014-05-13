import re
from ebnf.syntax import Syntax


class Parser(object):
    def __init__(self, filename, root=Syntax):
        # should parse according to standards in ebnf.ebnf
        text = open(filename, "rU").read()
        # remove the comments
        text = re.sub('\n\\s*#[^\n]*', '', '\n' + text)
        self.tree = root(None, text)
        self.compiled = {}

    def load_program(self, filename=None, text=None):
        if filename is not None:
            text = open(filename, "rU").read().strip()
        self.compiled[filename] = self.tree.compile(None, text)
        return self.compiled[filename]

    def run_program(self):
        pass

if __name__ == '__main__':
    ebnf = Parser('EBNFs/language.ebnf')
    print ebnf.load_program(text='((71.4*8.75)+7.3)')
