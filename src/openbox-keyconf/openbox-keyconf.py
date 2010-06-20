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

helptext="""M = [Mod3]
W = [Windows]
S = [Shift]
A = [Alt]
C = [Control]

F1,F2,F3,F4,F5,F6,F7,F8,F9,F10,F11,F12
Escape
Return
Menu
Tab
Pause
space
Print
Caps_Lock
Scroll_Lock
Num_Lock
Insert
Delete
BackSpace
Home  = [Pos1]
End   = [End]
Prior = [PageUp]
Next  = [PageDown]
asciicircum =  [^]
less        =  [<]
greater     =  [>]
minus       =  [-]
plus        =  [+]
comma       =  [,]
period      =  [.]
numbersign  =  [#]
acute       =  [´]

Left,Right,Up,Down
_____________________

[Keypad/Numberblock]

KP_0, KP_1, KP_2, KP_3, KP_4, KP_5, KP_6, KP_7, KP_8, KP_9
KP_Divide   = [/]
KP_Multiply = [*]
KP_Subtract = [-]
KP_Add      = [+]
KP_Enter
KP_Begin  = [5]
KP_Home   = [7]
KP_End    = [1]
KP_Prior  = [9] [PageUp]
KP_Next   = [3] [PageDown]
KP_Up     = [8] [cursor up]     
KP_Down   = [2] [cursor down]
KP_Left   = [4] [cursor left]
KP_Right  = [6] [cursor right]

for more keycodes start "xev" in a terminal"""

import lxadmin.defs as defs
import lxadmin.detect_os as detect_os

import gettext

gettext.bindtextdomain('lxadmin', defs.LOCALE_DIR)
gettext.textdomain('lxadmin')
_ = gettext.gettext

from gettext import gettext as _

import os
import sys
import time
import string
import codecs
import pygtk
pygtk.require('2.0')
import gtk
import pango
import gobject
import gc

configfile=detect_os.get_openbox_config():
mybuffer=None
helpwindow=None

def create_help_view(data=None):
    global helpwindow,mybuffer
    if mybuffer!=None: 
       helpwindow.show()
       helpwindow.present()
       return
    helpwindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
    helpwindow.set_title(_('Help: keyboard codes'))
    helpwindow.set_size_request(600,400)
    helpwindow.set_position(gtk.WIN_POS_CENTER_ALWAYS)
    helpwindow.connect("destroy", destroy_help_view)
    view=gtk.TextView()
    view.set_editable(False)
    view.set_cursor_visible(False)
    view.set_pixels_above_lines(0)
    view.set_pixels_below_lines(0)
    view.set_pixels_inside_wrap(0)
    view.set_wrap_mode(gtk.WRAP_NONE)
    font_desc = pango.FontDescription('Monospace 12')
    if font_desc:
       view.modify_font(font_desc)
    sw = gtk.ScrolledWindow()
    sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    sw.add(view)
    mybuffer=view.get_buffer()
    mybuffer.set_text(helptext)
    helpwindow.add(sw) 
    helpwindow.show_all()
    

def destroy_help_view(widget, data=None):
    global helpwindow,mybuffer
    helpwindow.destroy()
    helpwindow=None
    mybuffer=None



class Tool:

    def delete_event(self, widget, event, data=None):
        # If you return FALSE in the "delete_event" signal handler,
        # GTK will emit the "destroy" signal. Returning TRUE means
        # you don't want the window to be destroyed.
        # This is useful for popping up 'are you sure you want to quit?'
        # type dialogs.
        # Change FALSE to TRUE and the main window will not be destroyed
        # with a "delete_event".
        windowsize=self.window.get_size()
        windowpos=self.window.get_position()
        filenamen=home+'/.openbox-keyconf'
        f=file(filenamen,'w')
        if f:
           f.write('x=%i\n'      % windowpos[0])
           f.write('y=%i\n'      % windowpos[1])
           f.write('width=%i\n'  % windowsize[0])
           f.write('height=%i\n' % windowsize[1])
           f.close()
        return False


    def destroy(self, widget, data=None):
        #wird beim beenden ausgeführt
        gtk.main_quit()


    def goodbye(self,data=None):
        #Cancel Button is clicked
        if not self.delete_event(self.window,data):
           gtk.main_quit()


    def get_pathnumber(self,keycode):
        # return pathnumber of a given keycode
        for i in range(self.count_list):
            if self.liststore[i][0]==keycode: break
        if self.liststore[i][0]!=keycode: return -1  
        if self.liststore[i][3]=='add':   return -1
        return i


    def save(self,data=None):
        #Apply button is clicked
        filename=configfile
        text=''
        try:
           f=codecs.open(filename,'r','utf_8')
           text=f.read()
           config=text.split('\n')
           f.close()
        except:
           print "can't read",filename 
        for i in range(self.count_list):
            a=self.liststore[i][1]
            b=self.liststore[i][2]
            c=self.liststore[i][3]
            d=self.liststore[i][0]
            if c!='orginal':
               if c=='delete': print c,d 
               else: print a,b
        gc.collect()

        f=codecs.open(filename,'w','utf_8')
        found=False
        cutting=False 
        for line in config:
            if '<keyboard>' in line:
               found=True
               f.write(line+'\n')
               continue
            if '</keyboard>' in line:
               found=False
               # add keybinding code
               for i in range(self.count_list): 
                   s=self.liststore[i][3]
                   if s=='add':
                      f.write('    <keybind key="'+self.liststore[i][1]+'">\n')
                      a=self.liststore[i][2]
                      a=a.split('command=')
                      b=a[1].split(',)')
                      f.write('      <action name="Execute">\n')
                      f.write('        <command>'+b[0]+'</command>\n')
                      f.write('      </action>\n')
                      f.write('    </keybind>\n')
               f.write(line+'\n')
               continue
            if not found:
               f.write(line+'\n')
               continue
            if cutting:
               if '</keybind>' in line: cutting=False
               continue    
            if '<keybind ' in line: 
               lin=line.split('"')
               p=self.get_pathnumber(lin[1])
               if p==-1:
                  f.write(line+'\n')
                  continue
               s=self.liststore[p][3]
               if s=='orginal':
                  f.write(line+'\n')
                  continue
               if s=='delete':
                  cutting=True
                  continue 
               if s=='name':
                  f.write('    <keybind key="'+self.liststore[p][1]+'">\n')
                  continue
               if s=='execute':
                  f.write('    <keybind key="'+self.liststore[p][1]+'">\n')
                  a=self.liststore[p][2]
                  a=a.split('command=')
                  b=a[1].split(',)')
                  f.write('      <action name="Execute">\n')
                  f.write('        <command>'+b[0]+'</command>\n')
                  f.write('      </action>\n')
                  f.write('    </keybind>\n')
                  cutting=True
                  continue
            f.write(line+'\n')
        f.flush()
        f.close()
        os.system('openbox --reconfigure')
        self.goodbye()


    def mouse(self, widget, event, data=None):
        if event.button==1:
           # a keybinding in the treeview is clicked
           pathinfo=self.treeview.get_path_at_pos(int(event.x),int(event.y)) 
           if pathinfo==None: return False
           pathnr=pathinfo[0][0]  
           name=self.liststore[pathnr][1]
           action=self.liststore[pathnr][2]
           self.lock=True
           self.cb_exec.set_active(False)
           self.execute.set_sensitive(0)
           if 'command=' in action:
              a1=action.split('command=')
              a2=a1[1].split(',)')
              self.execute.set_text(a2[0])
              self.hbox.show()
           else: self.hbox.hide()
           self.path=pathnr
           self.keys.set_text(name)
           self.action.set_text(action)
           self.lock=False
   
    
    def row_activate(self, treeview, pathnr, column): 
           # a keybinding is selected by doubleclick or keyboard
           name=self.liststore[pathnr][1]
           action=self.liststore[pathnr][2]
           self.lock=True
           self.cb_exec.set_active(False)
           self.execute.set_sensitive(0)
           if 'command=' in action:
              a1=action.split('command=')
              a2=a1[1].split(',)')
              self.execute.set_text(a2[0])
              self.hbox.show()
           else: self.hbox.hide()
           self.path=pathnr
           self.keys.set_text(name)
           self.action.set_text(action)
           self.lock=False


    def keys_changed(self,data):
        if self.lock: return 
        if self.path==-1: return  
        a=self.keys.get_text() 
        a=a.strip()
        self.liststore[self.path][1]=a
        b=self.liststore[self.path][3]
        if b=='orginal': self.liststore[self.path][3]='name'


    def execute_entry_changed(self,data):
        if self.lock: return 
        if self.path==-1: return  
        a=self.execute.get_text() 
        a=a.strip()
        b='Execute(command='+a+',)'
        self.liststore[self.path][2]=b
        self.action.set_text(b)
        

    def add_new_keybinding(self,data=None):
        self.count_list+=1
        self.liststore.append(['F12','F12','Execute(command='+_("NameOfProgram")+',)','add'])     


    def delete_keybinding(self,data=None):
        if self.lock: return  
        if self.path==-1: return  
        self.hbox.hide()
        self.liststore[self.path][1]=""
        self.liststore[self.path][2]=""
        self.liststore[self.path][3]="delete"
        self.action.set_text('')
        self.keys.set_text('')


    def toggle_execute_entry(self,data=None):
        if self.lock: return 
        if self.path!=-1: b=self.liststore[self.path][3]
        s=self.cb_exec.get_active()
        if s: 
           self.execute.set_sensitive(1)
           if self.path!=-1:
              if (b=='orginal')or(b=='name'):
                  self.liststore[self.path][3]='execute'
        else: 
           self.execute.set_sensitive(0)
           if self.path!=-1:
              if (b=='execute'):
                  self.liststore[self.path][3]='name'


    def __init__(self):
        namen=home+'/.openbox-keyconf'
        if not os.access(namen,os.R_OK):
           f=file(namen,'w')
           f.write('x=0\n')
           f.write('y=0\n')
           f.write('width=800\n')
           f.write('height=400\n')
           f.close()
        f=file(namen,'r')
        s=f.readline()
        while s !='':
           s=s.replace('\n','')
           z=s.split('=')
           if z[0]=='x':       self.pos_x=int(z[1])
           if z[0]=='y':       self.pos_y=int(z[1])
           if z[0]=='width':   self.width=int(z[1])
           if z[0]=='height':  self.height=int(z[1])
           s=f.readline()
        f.close()

        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window=window
        vbox = gtk.VBox(False, 0)
        window.set_border_width(5)
        window.add(vbox)

        # When the window is given the "delete_event" signal (this is given
        # by the window manager, usually by the "close" option, or on the
        # titlebar), we ask it to call the delete_event () function
        # as defined above. The data passed to the callback
        # function is NULL and is ignored in the callback function.
        window.connect("delete_event", self.delete_event)
    
        # Here we connect the "destroy" event to a signal handler.  
        # This event occurs when we call gtk_widget_destroy() on the window,
        # or if we return FALSE in the "delete_event" callback.
        window.connect("destroy", self.destroy)
    
        # Sets the border width of the window.
        window.set_title(_('openbox keyboard bindings'))
        window.set_size_request(400,200)
        window.resize(self.width, self.height)
        window.move(self.pos_x,self.pos_y)

        self.liststore=gtk.ListStore(str,str,str,str)
        self.treeview=gtk.TreeView()
        self.treeview.set_headers_visible(True)
        self.treeview.set_model(self.liststore) 
        self.treeview.set_property('rules-hint',True)
        self.treeview.set_property('enable-grid-lines',True)
        self.treeview.connect('row-activated', self.row_activate)
        self.treeview.set_events(self.treeview.get_events() | gtk.gdk.BUTTON_PRESS_MASK)
        self.treeview.connect("button-press-event", self.mouse)
        self.cell1 = gtk.CellRendererText()
        self.cell2 = gtk.CellRendererText()
        self.spalte1 = gtk.TreeViewColumn(_('Key'))
        self.spalte2 = gtk.TreeViewColumn(_('Action'))
        self.treeview.append_column(self.spalte1)
        self.treeview.append_column(self.spalte2)
        self.spalte1.pack_start(self.cell1,True)
        self.spalte2.pack_start(self.cell2,True)
        self.spalte1.set_attributes(self.cell1, text=1)
        self.spalte2.set_attributes(self.cell2, text=2)
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.add(self.treeview)
        filename=configfile
        self.count_list=0
        try:
           f=codecs.open(filename,'r','utf_8')
           line=f.readline()
           found=False
           data='frog'
           action=False
           name=''
           while True: 
                 line=f.readline()
                 if not line: break
                 if '<keyboard>' in line:
                    found=True
                    continue
                 if '</keyboard>' in line: 
                    found=False
                 if not found: continue
                 lin=line.replace('\n','')
                 if '<keybind ' in lin:
                    lin2=lin.split('"') 
                    name=lin2[1]
                    action=False 
                    data=''
                    continue
                 if '</keybind>' in lin:                 
                    if action: data+=')'
                    if name!='': 
                       self.liststore.append([name,name,data,'orginal'])
                       self.count_list+=1
                    name=''
                    continue
                 if name!='':
                    if '</action>' in lin: continue
                    if '<action ' in lin:   
                       if action: data+='), ' 
                       action=True
                       lin2=lin.split('"') 
                       data=data+lin2[1]+'('
                       continue
                    if '<startupnotify>' in lin:
                       continue 
                    if '</startupnotify>' in lin:
                       continue 
                    if ('<' in lin) and ('>' in lin):
                       lin2=lin.split('<')
                       lin3=lin2[1].split('>')
                       data=data+lin3[0]+'='+lin3[1]+','
                 continue
           f.close()
        except:
           pass
        gc.collect()
        self.lock=True
        self.path=-1
        hbox = gtk.HBox(False, 5)
        self.keys=gtk.Entry(max=40)
        self.keys.connect("changed",self.keys_changed)
        self.action=gtk.Label('')
        hbox.pack_start(self.keys,False,False,0)
        hbox.pack_start(self.action,True,True,0)
        vbox.pack_start(hbox, False,False, 0)
        self.hbox = gtk.HBox(False, 5)
        self.cb_exec=gtk.CheckButton(_("Edit command")+" =")
        self.cb_exec.connect_object("toggled",self.toggle_execute_entry,None)
        self.execute=gtk.Entry(max=0) 
        self.execute.connect("changed",self.execute_entry_changed)
        self.hbox.pack_start(self.cb_exec,False,False,0)
        self.hbox.pack_start(self.execute,True,True,0)
        vbox.pack_start(self.hbox, False,False, 0)
        vbox.pack_start(sw, True, True, 0)
        hbox = gtk.HBox(False, 5)
        button1=gtk.Button(stock='gtk-apply')
        hiddenlabel=gtk.Label(' ')
        button2=gtk.Button(stock='gtk-cancel')
        button3=gtk.Button(stock='gtk-add')
        button4=gtk.Button(stock='gtk-delete')
        button5=gtk.Button(stock='gtk-help')
        hbox.pack_start(button1,False,False,0)
        hbox.pack_start(button3,False,False,0)
        hbox.pack_start(button4,False,False,0)
        hbox.pack_start(button5,False,False,0)
        hbox.pack_start(hiddenlabel,True,True,0)
        hbox.pack_start(button2,False,False,0)
        button1.connect_object("clicked", self.save,None)
        button2.connect_object("clicked", self.goodbye,None)
        button3.connect_object("clicked", self.add_new_keybinding,None)
        button4.connect_object("clicked", self.delete_keybinding,None)
        button5.connect("clicked", create_help_view)
        vbox.pack_end(hbox, False, False, 0)
        window.show_all() 
        self.hbox.hide()       


    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()



# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
     home=os.getenv("HOME")
     Elfriede = Tool()
     Elfriede.main()
