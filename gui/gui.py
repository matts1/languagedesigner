import gi
import os
from gi.repository import Gtk
import math, cairo
from ebnf.parse import Parser
import sys
from threading import Thread


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
        self.output_ele = glade.get_object("output").get_buffer()
        self.input_ele = glade.get_object('input')
        self.input_label_ele = glade.get_object('inputlabel')
        self.program_ele = self.program_obj.get_buffer()
        self.program_selector = glade.get_object("program_selector")
        self.program_ele.set_text('Click the new program button (top left) to start editing a new program (but first you need to save / open an E-BNF).')

        self.compiler = None
        self.directory = None
        self.program_name = None
        self.running = False

        self.glade = glade
        sys.path.append(sys.path[-1])  # replace this with something else later
        window = glade.get_object("main_window")
        window.show_all()
        window.maximize()

        self.open_ebnf('/ebnf/languages/language')

    #Quitting the application when the close button is pressed
    def gtk_main_quit(self, event):
        self.save(event)
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
        if not self.running:
            self.running = True
            compiled = self.compile(event)
            thread = Thread(target=self.compiler.run_program, args=(compiled,))
            thread.start()
            self.running = False

    def compile(self, event):
        self.compiler = Parser(self.get_text(self.ebnf_ele), file=False, language='', gui=self)
        self.tree_ele.set_text(repr(self.compiler.tree))
        self.compiled = self.compiler.load_program(self.get_text(self.program_ele))
        self.compiled_tree_ele.set_text(repr(self.compiled))
        return self.compiled

    def switch_program(self, event=None, name=None):
        if event is not None:
            name = event.get_active_text()
        self.program_name = name
        if name is not None:
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
        self.program_ele.set_text('Click the new program button (top left) to start editing a new program, or open a program in the top right drop down.')
        if isinstance(element, str):
            self.directory = '/'.join(__file__.split('/')[:-2]) + element
        else:
            self.directory = self.get_window(element).get_filename()
            self.close_window(element)
        assert os.path.isdir(self.directory)
        self.ebnf_text = open(self.directory + '/ebnf', 'rU').read()
        self.ebnf_ele.set_text(self.ebnf_text)
        sys.path[-1] = self.directory
        self.program_selector.remove_all()
        for program in os.listdir(self.directory + '/programs'):
            if program.endswith('.prog'):
                self.program_selector.append_text(program[:-5])


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

    def input_entered(self, *args):
        self.input_ele.entered = True

#running the GUI
if __name__ == "__main__":
    a = GUIGTK()
    Gtk.main()
