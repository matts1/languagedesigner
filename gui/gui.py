import gi
from gi.repository import Gtk
from ebnf.parse import Parser
import os


class GUIGTK:
    def __init__(self):
        #dictionary of all the handlers for the Glade events and the functions they call in the Python code
        dict = {
            "buttonClicked" : self.buttonClicked,
            "changed": self.buttonClicked,
            "backspace": self.buttonClicked,
            "activate": self.buttonClicked,
            "gtk_main_quit" : self.close,
            "railroad_selected" : self.stub,
            "draw_railroad": self.stub,
            "open_window": self.open_window,
            "close_window": self.close_window,
            "open_ebnf": self.open_ebnf,
            "open_program": self.open_program,
        }
        #setting up the glade file
        gladefile = "main3.glade"
        glade = Gtk.Builder()
        glade.add_from_file(gladefile)
        glade.connect_signals(dict)

        self.compiled_tree_ele = glade.get_object("compiled_parse_tree").get_buffer()
        self.tree_ele = glade.get_object("parse_tree").get_buffer()
        self.ebnf_ele = glade.get_object("ebnf").get_buffer()
        self.program_ele = glade.get_object("program").get_buffer()

        window = glade.get_object("main_window")
        window.show_all()
        window.maximize()


    #Quitting the application when the close button is pressed
    def close(self, event):
        Gtk.main_quit()

    def open_ebnf(self, element):
        fname = self.get_window(element).get_filename()
        assert not os.path.isdir(fname)
        self.close_window(element)
        self.compiler = Parser(fname, relative=False)
        self.ebnf_ele.set_text(self.compiler.text)

    def open_program(self, element):
        fname = self.get_window(element).get_filename()
        assert not os.path.isdir(fname)
        self.close_window(element)
        self.compiled = self.compiler.load_program(fname)
        self.program_ele.set_text(self.compiled)

    def stub(self, *args):
        pass

    def open_window(self, window):
        window.show_all()

    def get_window(self, window):
        while window.get_parent() is not None:
            window = window.get_parent()
        return window

    def close_window(self, element):
        self.get_window(element).hide()

    def open_railroad(self, widget, tab, tabindex):
        if tab.__class__.__name__ == 'DrawingArea':
            print "hello world"

    def buttonClicked(self, widget):
        print "hello world"

#running the GUI
if __name__ == "__main__":
    a = GUIGTK()
    Gtk.main()
