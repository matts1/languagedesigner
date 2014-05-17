import importlib
import re
from ebnf.syntax import Syntax
import sys

class Parser(object):
    def __init__(self, filename, root=Syntax, executor='executors'):
        # because somehow, 1000 isn't enough...
        sys.setrecursionlimit(int(1e5))

        # should parse according to standards in ebnf's ebnf
        self.language = filename
        text = open('languages/%s/ebnf' % filename, "rU").read()
        # remove the comments
        text = re.sub('\n\\s*#[^\n]*', '', '\n' + text)
        execute_nodes = {}
        self.state = object  # the class to create which stores the state
        try:
            module = vars(importlib.import_module('languages.%s.%s' % (self.language, executor)))
            for var in module:
                if var == 'State':
                    self.state = module[var]
                id = getattr(module[var], 'identifier', None)
                if id is not None:
                    execute_nodes[id] = module[var]
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
        program = self.compiled[filename]
        program.find_meta_children()
        program.run_tree('setup')
        return program

    def run_program(self, program_name, input=None, output=True):
        program = self.load_program(program_name)
        # execute_nodes is dict, metaidentifier -> executable class
        program.run_tree('create_state', self.state())
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
    compiler.run_program('test')
    compiler.run_program('average')

    compiler = Parser('language', executor='pseudocode')
    compiler.run_program('average')
