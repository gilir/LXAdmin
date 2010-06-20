#!/usr/bin/python
# -*- coding: UTF-8 -*-
#**************************************************************************
#                                                                         *
#   Copyright (c) 2010 by Elfriede Apfelkuchen                            *
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
import time
import codecs
import pygtk
pygtk.require('2.0')
import gtk
import pango

rot=[
"16 16 4 1",
". c #000000",
"# c #ff4040",
"a c None",
"b c #ffffff",
"aaaaa......aaaaa",
"aaa........bbaaa",
"aa...######bbbaa",
"a..##########bba",
"a..###bbb####bba",
"..###bbb######bb",
"..##bb########bb",
"..##bb########bb",
"..##b#########bb",
"..############bb",
"..############bb",
"a..##########bba",
"a..##########bba",
"aa...######bbbaa",
"aaa..bbbbbbbbaaa",
"aaaaabbbbbbaaaaa"]

gelb=[
"16 16 4 1",
". c #000000",
"# c #40a000",
"a c None",
"b c #ffffff",
"aaaaa......aaaaa",
"aaa........bbaaa",
"aa...######bbbaa",
"a..##########bba",
"a..###bbb####bba",
"..###bbb######bb",
"..##bb########bb",
"..##bb########bb",
"..##b#########bb",
"..############bb",
"..############bb",
"a..##########bba",
"a..##########bba",
"aa...######bbbaa",
"aaa..bbbbbbbbaaa",
"aaaaabbbbbbaaaaa"]

gruen=[
"16 16 4 1",
". c #000000",
"# c #00ff00",
"a c None",
"b c #ffffff",
"aaaaa......aaaaa",
"aaa........bbaaa",
"aa...######bbbaa",
"a..##########bba",
"a..###bbb####bba",
"..###bbb######bb",
"..##bb########bb",
"..##bb########bb",
"..##b#########bb",
"..############bb",
"..############bb",
"a..##########bba",
"a..##########bba",
"aa...######bbbaa",
"aaa..bbbbbbbbaaa",
"aaaaabbbbbbaaaaa"]

DefaultIcon=[
"16 16 4 1",
" 	c None",
".	c black",
"o	c white",
"O	c gray50",
"   .. .....     ",
"  .oo.ooooo.    ",
"  .ooooooooo.   ",
"  .oO.oooo..o.  ",
"   .. ....O ..  ",
"       ...   .  ",
"       ...      ",
"       ...      ",
"       ...      ",
"       ...      ",
"       ...      ",
"       ...      ",
"       ...      ",
"       ...      ",
"                ",
"                "]

runlevel=[]
def get_runlevel(pathname):
    global runlevel 
    for i in os.listdir(pathname):
        if len(i)>3:
           if (i[0]=='S'):
              runlevel.append(i[3:])


class startmenu:
    def destroy(self, widget, data=None):
        gtk.main_quit()


    def row_activate(self, treeview, path, column):
        # a service is doubleclicked...
        directory='/etc/init.d'
        name=self.liststore[path][4]
        state=self.liststore[path][0]
        if state==1:                   
           self.liststore[path][0]=0      #deactivate service
           self.liststore[path][1]=Soff
           os.rename(directory+os.sep+name,directory+os.sep+name+'_OFF')
           command=directory+os.sep+name+'_OFF'+ ' stop &'
           print command
           os.system(command.encode(codec1))
        else:
           self.liststore[path][0]=1      #activate service
           self.liststore[path][1]=Son
           os.rename(directory+os.sep+name+'_OFF',directory+os.sep+name)
           command=directory+os.sep+name+ ' start &'
           print command
           os.system(command.encode(codec1))


    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window=window
        window.set_title(_('Services')+' "/etc/init.d"')
        window.set_size_request(600,400)
        vbox = gtk.VBox(False, 10)
        window.add(vbox)
        window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        gtk.window_set_default_icon(gtk.gdk.pixbuf_new_from_xpm_data(DefaultIcon))
        self.liststore=gtk.ListStore(int,gtk.gdk.Pixbuf,str,str,str)
        self.treeview=gtk.TreeView()
        self.treeview.set_headers_visible(True)
        self.treeview.set_model(self.liststore)
        self.treeview.connect('row-activated', self.row_activate)
        self.cellpb = gtk.CellRendererPixbuf()
        self.cell1 = gtk.CellRendererText()
        self.cell2 = gtk.CellRendererText()
        self.cellpb.set_property('cell-background', 'grey80')
        self.cell1.set_property('cell-background', 'grey80')
        self.spalte1 = gtk.TreeViewColumn(_('Service'))
        self.spalte2 = gtk.TreeViewColumn(_('Description'))
        self.treeview.append_column(self.spalte1)
        self.treeview.append_column(self.spalte2)
        self.spalte1.pack_start(self.cellpb,False)
        self.spalte1.pack_start(self.cell1,True)
        self.spalte2.pack_start(self.cell2,True)
        self.spalte1.set_attributes(self.cellpb, pixbuf=1)
        self.spalte1.set_attributes(self.cell1, text=2)
        self.spalte2.set_attributes(self.cell2, text=3)
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.add(self.treeview)
        vbox.pack_start(sw , True, True, 0)
        window.connect("destroy", self.destroy)
        window.show_all()
        self.liststore.set_sort_column_id(2, gtk.SORT_ASCENDING)
        get_runlevel('/etc/rcS.d')
        get_runlevel('/etc/rc0.d')
        get_runlevel('/etc/rc1.d')
        get_runlevel('/etc/rc2.d')
        get_runlevel('/etc/rc3.d')
        get_runlevel('/etc/rc4.d')
        get_runlevel('/etc/rc5.d')
        get_runlevel('/etc/rc6.d')
        #print runlevel
        for i in os.listdir('/etc/init.d'):
            name=i.replace('_OFF','')
            try:
                name2=unicode(name,codec1)
            except:
                name2=name
            info='...'
            found=0
            try:
                f=codecs.open('/etc/init.d/'+i,'r','utf_8')
                text=f.read()
                f.close() 
                text=text.split('\n') 
                for line in text:
                    if '### BEGIN INIT INFO' in line: found=1
                    if '### END INIT INFO' in line: found=3
                    if (found == 0) or (found>2): continue
                    if '# Provides:' in line:
                       name2=line[11:]
                       name2=name2.replace('\t','')
                       name2=name2.strip() 
                       continue
                    if '# Short-Description:' in line:
                       text2=line[20:]
                       text2=text2.replace('\t','')
                       info=text2.strip()
                       continue
            except:
                print "error reading service: "+i
            if found==0:
               print 'ignore '+i
               continue

            nummer=1
            if '_OFF' in i: nummer=0
            try:
                if nummer==1:
                   if name in runlevel:
                      self.liststore.append([nummer,Son,name2,info,name])
                   else:
                      self.liststore.append([nummer,Son2,name2,info,name])
                else:
                   self.liststore.append([nummer,Soff,name2,info,name])
            except:
                pass
        userid=os.getuid()
        if userid!=0:
               dialog = gtk.MessageDialog(self.window, gtk.DIALOG_MODAL,gtk.MESSAGE_ERROR,gtk.BUTTONS_OK, "ERROR: not root!")
               result = dialog.run()
               dialog.destroy()



    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()



# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
     Soff=gtk.gdk.pixbuf_new_from_xpm_data(rot)
     Son2=gtk.gdk.pixbuf_new_from_xpm_data(gelb)
     Son =gtk.gdk.pixbuf_new_from_xpm_data(gruen)
     app=startmenu()
     app.main() 
