import importlib
import os
import re
from ebnf.syntax import Syntax
import sys

class Parser(object):
    def __init__(self, filename, root=Syntax, executor='executors', relative=True, canvas=None):
        # because somehow, 1000 isn't enough...
        sys.setrecursionlimit(int(1e5))
        self.root = root
        self.executor = executor

        # should parse according to standards in ebnf's ebnf
        self.language = filename
        if relative:
            self.directory = os.path.dirname(__file__) + '/languages/%s/' % filename
        else:
            self.directory = filename
        self.text = open(self.directory, "rU").read()
        self.compile_ebnf()

    def compile_ebnf(self):
        # remove the comments
        text = re.sub('\n\\s*#[^\n]*', '', '\n' + self.text)
        execute_nodes = {}
        self.state = object  # the class to create which stores the state
        try:
            module = vars(importlib.import_module('languages.%s.%s' % (self.language, self.executor)))
            for var in module:
                if var == 'State':
                    self.state = module[var]
                id = getattr(module[var], 'identifier', None)
                if id is not None:
                    execute_nodes[id] = module[var]
        except ImportError:
            pass
        self.tree = self.root(None, text, execute=execute_nodes, canvas=canvas)
        self.compiled = {}
        self.texts = {}

    def load_program(self, filename=None, text=None, relative=True):
        self.program_filename = filename
        if relative:
            text = open('%sprograms/%s.prog' % (self.directory, filename), "rU").read().strip()
        else:
            text = open(filename, 'rU').read().strip()
        self.program = text

    def compile_program(self, filename):
        program = self.tree.compile(None, self.program)
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
