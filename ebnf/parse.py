import re
from ebnf.syntax import Syntax


class Parser(object):
    def __init__(self, filename, root=Syntax):
        # should parse according to standards in ebnf.ebnf
        text = open(filename, "rU").read()
        # remove the comments
        text = re.sub('\n\\s*#[^\n]*', '', '\n' + text)
        self.tree = root(None, text)

    def load_program(self, filename):
        text = open(filename, "rU").read().strip()
        self.tree.text = text
        self.tree.parse_children()

if __name__ == '__main__':
    # ebnf = Parser('EBNFs/' + raw_input('Enter the filename to parse: ') + '.ebnf').tree
    # print ebnf
    # print input()
    ebnf = Parser('EBNFs/calculator.ebnf').tree
    print ebnf.compile(None, '(71.4*8.75)')
