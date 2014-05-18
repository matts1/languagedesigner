import gi
from gi.repository import Gtk
import math
import cairo
from ebnf.parse import Parser


class GUIGTK:

    def __init__(self):
        #dictionary of all the handlers for the Glade events and the functions they call in the Python code
        dict = { "buttonClicked" : self.buttonClicked,
                "changed": self.buttonClicked,
                "backspace": self.buttonClicked,
                "activate": self.buttonClicked,
                "gtk_main_quit" : self.close,
                "draw_railroad" : self.draw_railroad
        }
        #setting up the glade file
        gladefile = "main3.glade"
        glade = Gtk.Builder()
        glade.add_from_file(gladefile)
        #connecting the signals from the glade file with the python code
        glade.connect_signals(dict)
        #what is outputted in the ebnf window
        # ebnf = ("Here is where the "
        #         "ebnf will be going "parseebnf
        #         "some time in the "
        #         "future")
        self.compiler = Parser('language')
        self.compiled = self.compiler.run_program('average')
        lorem_ipsum = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam mollis volutpat nunc ac dignissim. "
                       "Vivamus sodales nulla rutrum mauris sagittis dictum. Ut nec condimentum mauris, a molestie odio."
                       " Nunc sit amet ultrices tortor, quis laoreet ipsum. Aliquam lobortis diam vitae arcu dignissim "
                       "consectetur. Integer bibendum gravida tellus at fermentum. Morbi lacinia ultricies purus, ut "
                       "tincidunt felis ullamcorper ut. Suspendisse semper bibendum dignissim.")
        glade.get_object("compiled_parse_tree").get_buffer().set_text(repr(self.compiled))
        glade.get_object("parse_tree").get_buffer().set_text(lorem_ipsum)
        glade.get_object("ebnf").get_buffer().set_text("E-BNF will go here")
        glade.get_object("program").get_buffer().set_text("Program will go here")
        window = glade.get_object("window1")
        window.show_all()
        window.maximize()


    #Quitting the application when the close button is pressed
    def close(self, event):
        print "Quitting"
        Gtk.main_quit()

    def draw_railroad(self, dwg_area, canvas):
        print "drawing"
        self.compiler.tree._canvas = canvas
        canvas.select_font_face("Courier New", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        canvas.set_font_size(14)
        self.compiler.tree.rdraw()


    def buttonClicked(self, widget):
        print "hello world"

#running the GUI
if __name__ == "__main__":
    a = GUIGTK()
    Gtk.main()