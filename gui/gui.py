import gi
import os
from gi.repository import Gtk
import math, cairo
from ebnf.parse import Parser
import sys


class GUIGTK:
    def __init__(self):
        #dictionary of all the handlers for the Glade events and the functions they call in the Python code
        handlers = dict([(fn, getattr(self, fn)) for fn in dir(self)])

        #setting up the glade file
        gladefile = "main3.glade"
        glade = Gtk.Builder()
        glade.add_from_file(gladefile)
        #connecting the signals from the glade file with the python code
        glade.connect_signals(handlers)

        self.compiled_tree_ele = glade.get_object("compiled_parse_tree").get_buffer()
        self.tree_ele = glade.get_object("parse_tree").get_buffer()
        self.ebnf_ele = glade.get_object("ebnf").get_buffer()
        self.program_obj = glade.get_object("program")
        self.program_ele = self.program_obj.get_buffer()
        self.program_ele.set_text('Click the new program button (top left) to start editing a new program (but first you need to save / open an E-BNF).')

        self.compiler = None
        self.directory = None
        self.program_name = None

        self.glade = glade
        sys.path.append(sys.path[-1])  # replace this with something else later
        window = glade.get_object("main_window")
        window.show_all()
        window.maximize()

    #Quitting the application when the close button is pressed
    def gtk_main_quit(self, event):
        Gtk.main_quit()

    quit = gtk_main_quit  # some event handlers call quit, others gtk_main_quit

    def save(self, event):
        f = open(self.directory + '/ebnf', 'w')
        f.write(self.get_text(self.ebnf_ele))
        f.close()
        if self.program_name is not None:
            f = open(self.directory + '/programs/%s.prog' % self.program_name, 'w')
            f.write(self.get_text(self.program_ele))
            f.close()

    def run(self, event):
        compiled = self.compile(event)
        self.compiler.run_program(compiled, file=False)

    def compile(self, event):
        self.compiler = Parser(self.get_text(self.ebnf_ele), file=False, language='')
        self.tree_ele.set_text(repr(self.compiler.tree))
        self.compiled = self.compiler.load_program(self.get_text(self.program_ele), file=False)
        self.compiled_tree_ele.set_text(repr(self.compiled))
        return self.compiled

    def switch_program(self, event=None, name=None):
        if event is not None:
            pass  # get name
        self.program_name = name
        self.program_ele.set_text(open(self.directory + '/programs/%s.prog' % name, 'rU').read())


    def do_new_program(self, event):
        name = self.traverse(event, '^^01').get_text()
        assert name  # can't be empty
        open(self.directory + '/programs/%s.prog' % name, 'w').close()  # create the file
        self.program_ele.set_text('')
        self.switch_program(name=name)

    def do_saveas(self, event):
        pass

    def draw_railroad(self, dwg_area, canvas):
        if self.compiler is not None and False:  # don't do this for now
            self.compiler.tree._canvas = canvas
            canvas.select_font_face("Courier New", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            canvas.set_font_size(14)
            self.compiler.tree.rdraw()

    def open_ebnf(self, element):
        if self.directory is None:
            self.program_ele.set_text('Click the new program button (top left) to start editing a new program.')
        self.directory = self.get_window(element).get_filename()
        assert os.path.isdir(self.directory)
        self.ebnf_text = open(self.directory + '/ebnf', 'rU').read()
        self.close_window(element)
        self.ebnf_ele.set_text(self.ebnf_text)
        sys.path[-1] = self.directory

    def open_window(self, window):
        window.show_all()

    def get_window(self, window):
        while window.get_parent() is not None:
            window = window.get_parent()
        return window

    def close_window(self, element):
        self.get_window(element).hide()

    def traverse(self, event, route):
        for letter in route:
            if letter == '^':
                event = event.get_parent()
            else:
                event = event.get_children()[int(letter)]
        return event

    def get_text(self, buffer):
        return buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)

#running the GUI
if __name__ == "__main__":
    a = GUIGTK()
    Gtk.main()
