import gi
import os
from gi.repository import Gtk
import math, cairo
from ebnf.parse import Parser


class GUIGTK:
    def __init__(self):
        #dictionary of all the handlers for the Glade events and the functions they call in the Python code
        dict = {
            "gtk_main_quit" : self.close,
            "draw_railroad": self.draw_railroad,
            "open_window": self.open_window,
            "close_window": self.close_window,
            "open_file": self.open_file,
            "open_ebnf_window": self.open_ebnf_window,
            "open_program": self.open_program,
            "open_program_window": self.open_program_window,
        }
        #setting up the glade file
        gladefile = "main3.glade"
        glade = Gtk.Builder()
        glade.add_from_file(gladefile)
        #connecting the signals from the glade file with the python code
        glade.connect_signals(dict)

        self.compiled_tree_ele = glade.get_object("compiled_parse_tree").get_buffer()
        self.tree_ele = glade.get_object("parse_tree").get_buffer()
        self.ebnf_ele = glade.get_object("ebnf").get_buffer()
        self.program_ele = glade.get_object("program").get_buffer()

        self.compiler = None
        self.compiled = None
        self.opening_program = False

        self.program_text = self.program_file = self.ebnf_text = self.ebnf_file = None

        window = glade.get_object("main_window")
        window.show_all()
        window.maximize()

    #Quitting the application when the close button is pressed
    def close(self, event):
        Gtk.main_quit()

    def draw_railroad(self, dwg_area, canvas):
        if self.compiler is not None:
            self.compiler.tree._canvas = canvas
            canvas.select_font_face("Courier New", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            canvas.set_font_size(14)
            self.compiler.tree.rdraw()

    def open_file(self, element):
        return self.open_program(element) if self.opening_program else self.open_ebnf(element)

    def open_ebnf(self, element):
        fname = self.get_window(element).get_filename()
        self.ebnf_file = fname
        self.ebnf_text = open(fname, 'rU').read()
        assert not os.path.isdir(fname)
        self.close_window(element)
        # self.compiler = Parser(self.ebnf_text, file=False)
        self.ebnf_ele.set_text(self.ebnf_text)

    def open_program(self, element):
        fname = self.get_window(element).get_filename()
        assert not os.path.isdir(fname)
        self.close_window(element)
        self.program_file = fname
        self.program_text = open(fname, 'rU').read().strip()
        # self.compiled = self.compiler.load_program(self.program_text, file=False)
        self.program_ele.set_text(self.program_text)

    def open_ebnf_window(self, window):
        self.opening_program = False
        self.open_window(window)

    def open_program_window(self, window):
        self.opening_program = True
        self.open_window(window)

    def open_window(self, window):
        window.show_all()

    def get_window(self, window):
        while window.get_parent() is not None:
            window = window.get_parent()
        return window

    def close_window(self, element):
        self.get_window(element).hide()

#running the GUI
if __name__ == "__main__":
    a = GUIGTK()
    Gtk.main()
