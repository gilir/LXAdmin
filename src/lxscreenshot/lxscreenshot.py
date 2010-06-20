#!/usr/bin/python
# -*- coding: UTF-8 -*-
#**************************************************************************
#                                                                         *
#   Copyright (c) Februar 2008 by Elfriede Apfelkuchen                    *
#                                                                         *
#   This program is free software: you can redistribute it and/or modify  *
#   it under the terms of the GNU General Public License as published by  *
#   the Free Software Foundation, either version 3 of the License, or     *
#   (at your option) any later version.                                   *
#                                                                         *
#   This program is distributed in the hope that it will be useful,       *
#   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#   GNU General Public License for more details.                          *
#                                                                         *
#   You should have received a copy of the GNU General Public License     *
#   along with this program.  If not, see <http://www.gnu.org/licenses/>. *
#                                                                         *
#**************************************************************************
import lxadmin.defs as defs

import gettext

gettext.bindtextdomain('lxadmin', defs.LOCALE_DIR)
gettext.textdomain('lxadmin')
_ = gettext.gettext

from gettext import gettext as _

import os
import sys
import string
import pygtk
pygtk.require('2.0')
import gtk
import codecs
import gobject

DefaultIcon=[
"16 14 4 1",
" 	c None",
".	c black",
"X	c white",
"o	c gray50",
"      ......    ",
"     .XXXXXX.   ",
" ....Xo...oX... ",
".XXXX.......XXX.",
".......ooo......",
".Xoo..oXXoo..oo.",
".Xoo..oXooo..oo.",
".Xoo..ooooo..oo.",
".Xooo..ooo..ooo.",
".Xooo.......ooo.",
".Xooooo...ooooo.",
" .............. ",
"                ",
"                "]

class Simple:

    def destroy(self, widget, data=None):
        #wird beim beenden ausgeführt
        gtk.main_quit()

    def registerStock(self,namen,text,icon):
        #registriert eine Standart-Button-Beschriftung mit icon
        items = [(namen, text, 0, 0, '')]
        # Register our stock items
        gtk.stock_add(items)
        # Add our custom icon factory to the list of defaults
        factory = gtk.IconFactory()
        factory.add_default()
        pixbuf=gtk.gdk.pixbuf_new_from_xpm_data(icon)
        icon_set = gtk.IconSet(pixbuf)
        factory.add(namen, icon_set)

    def start(self,data):
        #screenshot angeklickt, verstecke Fenster und starte self.screenshot mit 0.5s Verzögerung
        self.source_id = gobject.timeout_add(500, self.screenshot)
        self.window.hide()

    def screenshot(self):
        #jetzt wird der screenshot tatsächlich ausgeführt
        home=os.getenv("HOME")
        filename=os.path.join(home,"screenshot-01.png")
        i=1
        while os.path.exists(filename):
              i+=1     
              filename=os.path.join(home,"screenshot-%02i.png" % i)
        rootWindow = gtk.gdk.get_default_root_window()
        width=gtk.gdk.screen_width()
        height=gtk.gdk.screen_height()
        pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,width,height)
        pixbuf.get_from_drawable(rootWindow,rootWindow.get_colormap(),0,0,0,0,width,height)
        pixbuf.save(filename,"png")
        print filename
        dialog = gtk.MessageDialog(self.window, gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,gtk.BUTTONS_OK, filename)
        result = dialog.run()
        dialog.destroy()
        gtk.main_quit()
        return False

    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window=window
        window.set_title(_('Screenshot'))
        bbox=gtk.HBox(False,0)
        window.add(bbox)
        window.connect("destroy", self.destroy)
        self.registerStock('cat-screenshot',_('_Screenshot'),DefaultIcon) 
        button1=gtk.Button(stock='cat-screenshot')
        button2=gtk.Button(stock='gtk-cancel')
        bbox.pack_start(button1,True,True,0)
        bbox.pack_start(button2,True,True,0)
        button1.connect('clicked',self.start)
        button2.connect('clicked',self.destroy)
        window.set_border_width(5)
        window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        gtk.window_set_default_icon(gtk.gdk.pixbuf_new_from_xpm_data(DefaultIcon))
        window.set_resizable(False)
        window.show_all()

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()


# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
     app = Simple()
     app.main()
