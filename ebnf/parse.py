import imp
import os
import re
from ebnf.syntax import Syntax
import sys
import traceback as tb

class Parser(object):
    def __init__(self, filename, root=Syntax, executor='executors', file=True, canvas=None, language=None, gui=None, directory=None):
        """
        Creates a parser object which has access to the parse tree. Also compiles the EBNF
        """
        # because somehow, 1000 isn't enough...
        sys.setrecursionlimit(int(1e5))
        self.root = root
        self.executor = executor
        self.canvas = canvas
        self.file = file
        self.gui = gui

        # should parse according to standards in ebnf's ebnf
        self.language = ('languages.%s.' % filename) if language is None else language
        if file:
            self.directory = os.path.dirname(__file__) + '/languages/%s/' % filename
            self.text = open(self.directory + 'ebnf', "rU").read()
        else:
            if not directory.endswith('/'):
                directory += '/'
            self.directory = directory
            self.text = filename
        self.compile_ebnf()

    def compile_ebnf(self):
        # remove the comments
        text = re.sub('\n\\s*#[^\n]*', '', '\n' + self.text)
        execute_nodes = {}
        self.state = object  # the class to create which stores the state
        try:
            module = vars(imp.load_source('executor', self.directory + self.executor + '.py'))
            for var in module:
                if var == 'State':
                    self.state = module[var]
                id = getattr(module[var], 'identifier', None)
                if id is not None:
                    execute_nodes[id] = module[var]
        except ImportError:
            print 'Import of %s failed. You will be unable to run programs' % (self.directory + self.executor + '.py')
        self.tree = self.root(None, text, execute=execute_nodes, canvas=self.canvas)
        self.compiled = {}
        self.texts = {}

    def load_program(self, filename=None):
        """
        Loads and compiles a program into the compiler. Does not run it
        """
        self.program_filename = filename
        if self.file:
            self.program = open('%sprograms/%s.prog' % (self.directory, filename), "rU").read().strip()
        else:
            self.program = filename
        return self.compile_program(filename)

    def compile_program(self, filename):
        self.program = self.tree.compile(None, self.program, gui=self.gui)
        self.program.find_meta_children()
        self.program.run_tree('setup')
        return self.program

    def run_program(self, program, input=None, output=True):
        """
        Calls load program then runs the program
        """
        if self.file:
            program = self.load_program(program)
        # execute_nodes is dict, metaidentifier -> executable class
        try:
            program.run_tree('create_state', self.state())
            program.execute()
            program.run_tree('teardown')
            program.output('program finished with exit code 0')
        except Exception as e:
            exc_traceback = ''.join(tb.format_list(tb.extract_tb(sys.exc_info()[2])))
            if self.gui is not None:
                self.gui.output_ele.set_text(
                    self.gui.get_text(self.gui.output_ele) +
                    '\n\nRuntime Error\n\n%s\n\n%s' % (
                        exc_traceback,
                        e.message
                    )
                )
            else:
                print exc_traceback
                raise e
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
