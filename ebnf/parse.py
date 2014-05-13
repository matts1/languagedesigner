import importlib
import re
from ebnf.syntax import Syntax


class Parser(object):
    def __init__(self, filename, root=Syntax):
        # should parse according to standards in ebnf's ebnf
        self.language = filename
        text = open('languages/%s/ebnf' % filename, "rU").read()
        # remove the comments
        text = re.sub('\n\\s*#[^\n]*', '', '\n' + text)
        self.tree = root(None, text)
        self.compiled = {}

    def load_program(self, filename=None, text=None):
        if filename is not None:
            text = open('languages/%s/programs/%s.prog' % (self.language, filename), "rU").read().strip()
        self.compiled[filename] = self.tree.compile(None, text)
        return self.compiled[filename]

    def run_program(self, program_name, input=None, output=True):
        # execute_nodes is dict, metaidentifier -> executable class
        execute_nodes = {}
        module = vars(importlib.import_module('languages.%s.executors' % self.language))
        for var in module:
            if not var.startswith('__'):
                var = module[var]
                id = getattr(var, 'identifier', None)
                if id is not None:
                    execute_nodes[id] = var
        return output  # TODO: make this the program output

    def test(self):
        # look for .in and .out files that match .prog files
        self.run_program(input=None, output=False)

if __name__ == '__main__':
    import sys
    sys.setrecursionlimit(int(1e5))
    compiler = Parser('calculator')
    compiler.load_program('1')
    compiler.run_program('1')
