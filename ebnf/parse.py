import importlib
import re
from ebnf.syntax import Syntax
import sys

class Parser(object):
    def __init__(self, filename, root=Syntax):
        # because somehow, 1000 isn't enough...
        sys.setrecursionlimit(int(1e5))

        # should parse according to standards in ebnf's ebnf
        self.language = filename
        text = open('languages/%s/ebnf' % filename, "rU").read()
        # remove the comments
        text = re.sub('\n\\s*#[^\n]*', '', '\n' + text)
        execute_nodes = {}
        try:
            module = vars(importlib.import_module('languages.%s.executors' % self.language))
            for var in module:
                if not var.startswith('__'):
                    var = module[var]
                    id = getattr(var, 'identifier', None)
                    if id is not None:
                        execute_nodes[id] = var
        except ImportError:
            pass
        self.tree = root(None, text, execute=execute_nodes)
        self.compiled = {}

    def load_program(self, filename=None, text=None):
        if filename is not None and filename in self.compiled:
            return self.compiled[filename]
        if filename is not None:
            text = open('languages/%s/programs/%s.prog' % (self.language, filename), "rU").read().strip()
        self.compiled[filename] = self.tree.compile(None, text)
        return self.compiled[filename]

    def run_program(self, program_name, input=None, output=True):
        program = self.load_program(program_name)
        # execute_nodes is dict, metaidentifier -> executable class
        program.find_meta_children()
        program.run_tree('setup')
        program.execute()
        program.run_tree('teardown')
        # TODO: make this function return the program output
        return program

    def test(self):
        # look for .in and .out files that match .prog files
        self.run_program(input=None, output=False)

if __name__ == '__main__':
    compiler = Parser('calculator')
    compiler.run_program('1')
    compiler.run_program('2')
    compiler = Parser('language')
    print compiler.run_program('test')
    compiler.run_program('average')
