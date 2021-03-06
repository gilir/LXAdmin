#!/usr/bin/python
# -*- coding: UTF-8 -*-
#**************************************************************************
#                                                                         *
#   Copyright (c) 2010 by Elfriede Apfelkuchen <elfriede@sidux.com>       *
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
import lxadmin.detect_os as detect_os 

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
import pango

control_center_icons=[
["name","icon","command"],
[_("Login Screen"),"config-users", detect_os.get_command_su() + " /usr/bin/lxdmconf"],
[_("Configure Openbox"),"obconf",'obconf'],
[_("Preferred Applications"),"applications-system",'libfm-pref-apps'],
[_("Openbox Keyboard Shortcuts"),"input-keyboard",'openbox-keyconf'],
[_("Keyboard Layout"),"input-keyboard",'lxkeyboardconf'],
[_("Mouse&Keyboard"),"input-keyboard",'lxinput'],
[_("Set Wallpaper"),"desktop",'pcmanfm --desktop-pref'],
[_("Screensaver Settings"),"xscreensaver",'xscreensaver-demo'],
[_("Appearance"),"preferences-desktop-theme",'lxappearance'],
[_("configure Fonts"),"format-text-bold",'lxfontconfig'],
[_("PCManFM Settings"),"file-manager",'pcmanfm --show-pref=1'],
[_("PCManFM Superuser Mode"),"file-manager", detect_os.get_command_su() + " pcmanfm --no-desktop"],
[_("Refresh Panel"),"gtk-refresh",'lxpanelctl restart'],
[_("Search Software"),"search", detect_os.get_search_software()],
[_("Session Settings"),"gnome-window-manager",'lxsession-edit'],
[_("Monitor Settings"),"computer",'lxrandr'],
]
#TODO Let's the user define it's own progams

class Simple:

    def destroy(self, widget, data=None):
        #wird beim beenden ausgeführt
        gtk.main_quit()


    def mouse(self, widget, event, data=None):
        if event.button==1:
           pathinfo=widget.get_path_at_pos(int(event.x),int(event.y)) 
           if pathinfo==None: return False
           pathnr=pathinfo[0]  
           command=self.liststore[pathnr][2]
           if command=='xscreensaver-demo':
              if not os.path.exists('/usr/bin/xscreensaver-demo'):
                 dialog = gtk.MessageDialog(self.window, gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,gtk.BUTTONS_OK, "apt-get install xscreensaver")
                 result = dialog.run()
                 dialog.destroy()
           os.system(command+' &') 
           return True
        return False


    def __init__(self):
        # create a new window
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window=window
        window.set_title(_('LXDE-Control-Center'))
        window.connect("destroy", self.destroy)
        window.set_border_width(3)
        window.set_position(gtk.WIN_POS_CENTER_ALWAYS)

        it=gtk.icon_theme_get_default()
        gtk.window_set_default_icon(it.load_icon("gtk-preferences",48,gtk.ICON_LOOKUP_FORCE_SVG))
        window.resize(800,400)
        self.liststore=gtk.ListStore(gtk.gdk.Pixbuf,str,str)
        self.iv=gtk.IconView(self.liststore)
        self.iv.set_pixbuf_column(0)
        self.iv.set_text_column(1)
        self.iv.set_events(self.iv.get_events() | gtk.gdk.BUTTON_PRESS_MASK)
        self.iv.connect("button-press-event", self.mouse)
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.add(self.iv)
        window.add(sw)

        first=True
        for line in control_center_icons:
            if first:
               first=False
               continue  
            try:
               if '/' in line[1]:
                  pixbuf=gtk.gdk.pixbuf_new_from_file(line[1])
               else:
                  pixbuf=it.load_icon(line[1],48,gtk.ICON_LOOKUP_FORCE_SVG)
            except:
               pixbuf=it.load_icon('gtk-stop',48,gtk.ICON_LOOKUP_FORCE_SVG)
            namen=(line[0])
            self.liststore.append([ pixbuf,namen,line[2] ])
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
