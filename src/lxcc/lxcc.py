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

control_center_icons=[
["name","icon","command"],
["Login Screen","config-users",'su-to-root -X -c "/usr/bin/lxdmconf"'],
["Configure Openbox","obconf",'obconf'],
["Preferred Applications","applications-system",'libfm-pref-apps'],
["Openbox Keyboard Shortcuts","input-keyboard",'openbox-keyconf'],
["Keyboard Layout","input-keyboard",'keyboardconf'],
["Mouse&Keyboard","input-keyboard",'lxinput'],
["Set Wallpaper","desktop",'pcmanfm --desktop-pref'],
["Screensaver Settings","xscreensaver",'xscreensaver-demo'],
["Appearance","preferences-desktop-theme",'lxappearance'],
["configure Fonts","format-text-bold",'fontconfig.py'],
["PCManFM Settings","file-manager",'pcmanfm --show-pref=1'],
["PCManFM Superuser Mode","file-manager",'su-to-root -X -c "pcmanfm --no-desktop"'],
["Refresh Panel","gtk-refresh",'lxpanelctl restart'],
["Search Software","search",'apt-leo'],
["Session Settings","gnome-window-manager",'lxsession-edit'],
["Monitor Settings","computer",'lxrandr'],
]




import locale
locale.setlocale(locale.LC_ALL, '')   #set locale from 'LANG'
Xcodec=locale.getpreferredencoding(False)
import os
import sys
import string
import pygtk
pygtk.require('2.0')
import gtk
import codecs
import pango

from gettext import gettext as _

I18N={}

def i18n(text):
    #liefert einen Internationialisierungstext zurück
    if I18N_ready:
       if I18N.has_key(text): return I18N[text]
       else: return text
    else: return text

def load_i18n(filename):
     #lädt das Internationalisierung.moo file
     ready=False
     lang=os.getenv('LANG')
     if not lang: return ready
     lang2='/usr/share/locale/'+lang[0:2] +'/LC_MESSAGES/'+filename
     lang3='/usr/share/locale/'+lang[0:5] +'/LC_MESSAGES/'+filename
     lang='no file'
     if   os.access(lang3,os.R_OK): lang=lang3
     elif os.access(lang2,os.R_OK): lang=lang2
     if lang != 'no file':
        f=codecs.open(lang,'r','utf_8')
        if f:
           lang=f.readlines()
           f.close()
           ready=True
           for z in lang:
               s=z.replace('\n','').split('=')
               if s[0]=='': continue
               I18N[s[0]]=s[1]
     return ready


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
            namen=i18n(line[0])
            self.liststore.append([ pixbuf,namen,line[2] ])
        window.show_all()


    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()


# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
     I18N_ready = load_i18n('lxcc.moo')
     app = Simple()
     app.main()
