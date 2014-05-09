# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

from locale import gettext as _

from gi.repository import Gtk # pylint: disable=E0611
import logging
logger = logging.getLogger('language')

from language_lib import Window
from language.AboutLanguageDialog import AboutLanguageDialog
from language.PreferencesLanguageDialog import PreferencesLanguageDialog

# See language_lib.Window.py for more details about how this class works
class LanguageWindow(Window):
    __gtype_name__ = "LanguageWindow"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(LanguageWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutLanguageDialog
        self.PreferencesDialog = PreferencesLanguageDialog

        # Code for other initialization actions should be added here.

