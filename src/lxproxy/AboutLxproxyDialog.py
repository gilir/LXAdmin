# -*- coding: utf-8 -*-
### BEGIN LICENSE
# Copyright (C) YYYY Leszek Lesner leszek@zevenos.com
#This program is free software: you can redistribute it and/or modify it 
#under the terms of the GNU General Public License version 3, as published 
#by the Free Software Foundation.
#
#This program is distributed in the hope that it will be useful, but 
#WITHOUT ANY WARRANTY; without even the implied warranties of 
#MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
#PURPOSE.  See the GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License along 
#with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

import sys
import os
import gtk

from lxproxyconfig import getdatapath

class AboutLxproxyDialog(gtk.AboutDialog):
    __gtype_name__ = "AboutLxproxyDialog"

    def __init__(self):
        """__init__ - This function is typically not called directly.
        Creation of a AboutLxproxyDialog requires redeading the associated ui
        file and parsing the ui definition extrenally, 
        and then calling AboutLxproxyDialog.finish_initializing().
    
        Use the convenience function NewAboutLxproxyDialog to create 
        NewAboutLxproxyDialog objects.
    
        """
        pass

    def finish_initializing(self, builder):
        """finish_initalizing should be called after parsing the ui definition
        and creating a AboutLxproxyDialog object with it in order to finish
        initializing the start of the new AboutLxproxyDialog instance.
    
        """
        #get a reference to the builder and set up the signals
        self.builder = builder
        self.builder.connect_signals(self)

        #code for other initialization actions should be added here

def NewAboutLxproxyDialog():
    """NewAboutLxproxyDialog - returns a fully instantiated
    AboutLxproxyDialog object. Use this function rather than
    creating a AboutLxproxyDialog instance directly.
    
    """

    #look for the ui file that describes the ui
    ui_filename = os.path.join(getdatapath(), 'ui', 'lxproxy', 'AboutLxproxyDialog.ui')
    if not os.path.exists(ui_filename):
        ui_filename = None

    builder = gtk.Builder()
    builder.add_from_file(ui_filename)    
    dialog = builder.get_object("about_lxproxy_dialog")
    dialog.finish_initializing(builder)
    return dialog

if __name__ == "__main__":
    dialog = NewAboutLxproxyDialog()
    dialog.show()
    gtk.main()

