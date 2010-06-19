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

import os
import sys
import time
import string
import codecs
import pygtk
pygtk.require('2.0')
import gtk
import pango
import gc

import gettext
import lxadmin.defs as defs

gettext.bindtextdomain('lxadmin', defs.LOCALE_DIR)
gettext.textdomain('lxadmin')
_ = gettext.gettext


def finden(arg,dir,filenames):
    #subprocess of os.path.walk: get filenames in directorys
    global fileliste
    for text in filenames: 
        filename=dir+os.sep+text
        if os.path.isdir(filename): continue
        fileliste.append(filename)

def get_themes(picturepath):
    #get filenames of all pictures in picturepath
    global fileliste
    fileliste=[]
    os.path.walk(picturepath,finden,True)
    themes=[]
    for line in fileliste:
        if ('.jpg' in line) or ('.png' in line) or ('.gif' in line) or ('.JPG' in line):
           themes.append(line)
    return themes

def get_gtk2_themes():
    #give all gtk2 Themes as List back
    themes=[]
    for line in os.listdir('/usr/share/themes'):
        if os.access('/usr/share/themes/'+line+'/gtk-2.0/gtkrc',os.R_OK):
           themes.append(os.path.basename(line))
    return themes

def get_lxdm_themes():
    #give all lxdm Themes as List back
    themes=[]
    try:
       for line in os.listdir('/usr/share/lxdm/themes'):
           if os.access('/usr/share/lxdm/themes/'+line+'/gtkrc',os.R_OK):
              themes.append(os.path.basename(line))
    except:
       return ['off'] 
    return themes

def read_entry(config,confkey,keydefault):
    #read a config entry
    l=len(confkey)
    antwort=keydefault
    for line in config:
        if len(line)<l: continue
        if line[0:1]=='#': continue
        if line[0:l]==confkey: antwort=line[l:]   
    return antwort

def write_entry(config,section,confkey,keyvalue):
    #write a config entry into section
    myconfig=[]
    found=False
    mysection='[Flag]'
    l=len(confkey) 
    print 'write'+section+':',confkey+keyvalue
    for line in config:
        if len(line)>2:
           if line[0]=='[':
              newsection=line.strip()
              if mysection==section:
                 if found==False: 
                    myconfig.append(confkey+keyvalue)
                    found=True
              mysection=newsection
              myconfig.append(line)
              continue 
        if len(line)<l:
           myconfig.append(line)
           continue
        if (line[0:l]==confkey) and (mysection==section):
           found=True
           myconfig.append(confkey+keyvalue)
           continue
        myconfig.append(line)
    if found==False: 
       myconfig.append(confkey+keyvalue)
    return myconfig

def delete_entry(config,confkey):
    #delete a config entry
    myconfig=[]
    found=False
    l=len(confkey) 
    for line in config:
        if len(line)<l:
           myconfig.append(line)
           continue
        if line[0:l]==confkey:
           found=True
           continue
        myconfig.append(line)
    return myconfig
 
 
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
        home=os.getenv('HOME')
        home=home+'/.lxdmconf'
        f=file(home,'w')
        if f:
           f.write('x=%i\n'      % windowpos[0])
           f.write('y=%i\n'      % windowpos[1])
           f.write('width=%i\n'  % windowsize[0])
           f.write('height=%i\n' % windowsize[1])
           f.close()
        return False

    def destroy(self, widget, data=None):
        #wird beim beenden ausgefÃ¼hrt
        gtk.main_quit()

    def goodbye(self,data=None):
        #Cancel Button is clicked
        if not self.delete_event(self.window,data):
           gtk.main_quit()


    def save(self,data=None):
        #Apply Button is clicked
        print '==================================='       
        os.system('mkdir  /etc/lxdm.d  2>/dev/null')

        if self.cb_numlock.get_active(): 
           self.config=write_entry(self.config,'[base]','numlock=','1')
        else:
           self.config=write_entry(self.config,'[base]','numlock=','0')

        if self.cb_lang.get_active(): 
           self.config=write_entry(self.config,'[display]','lang=','1')
        else:
           self.config=write_entry(self.config,'[display]','lang=','0')

        if self.cb_bottom.get_active(): 
           self.config=write_entry(self.config,'[display]','bottom_pane=','1')
        else:
           self.config=write_entry(self.config,'[display]','bottom_pane=','0')

        if self.cb_autologin.get_active(): 
           a=self.entryuser.get_text()
           a=a.strip()
           self.config=write_entry(self.config,'[base]','autologin=',a)
        else:
           self.config=delete_entry(self.config,'autologin=')      

        a=self.entrysession.get_text()
        a=a.strip()
        if self.cb_session.get_active():
           self.config=write_entry(self.config,'[base]','session=',a)
        else:
           self.config=delete_entry(self.config,'session=')

        model = self.combobox.get_model()
        index = self.combobox.get_active()
        theme=model[index][0]
        self.config=write_entry(self.config,'[display]','bg=',theme)

        model = self.comboboxLXDM.get_model()
        index = self.comboboxLXDM.get_active()
        theme=model[index][0]
        self.config=write_entry(self.config,'[display]','theme=',theme)

        model = self.comboboxGTK.get_model()
        index = self.comboboxGTK.get_active()
        theme=model[index][0]
        self.config=write_entry(self.config,'[display]','gtk_theme=',theme)

        f=codecs.open('/etc/lxdm/lxdm.conf','w','utf_8')
        for line in self.config:
            text=line+'\n'
            f.write(text)
        f.close()
        #gtk.main_quit()
        self.goodbye()


    def read_config(self):
        filename='/etc/lxdm.d/lxdm_custom.conf'
        if not os.access(filename,os.R_OK): filename='/etc/lxdm/lxdm.conf'
        f=codecs.open(filename,'r','utf_8')
        text=f.read()
        f.close()
        self.config=text.split('\n')

        a=read_entry(self.config,"numlock=","0")
        a=a.replace('\t', ' ')
        a=a.strip()
        print 'numlock=',a
        if a=='1': 
           self.cb_numlock.set_active(True)

        a=read_entry(self.config,"lang=","1")
        a=a.replace('\t', ' ')
        a=a.strip()
        print 'lang=',a
        if a=='1': 
           self.cb_lang.set_active(True)

        a=read_entry(self.config,"bottom_pane=","1")
        a=a.replace('\t', ' ')
        a=a.strip()
        print 'bottom_pane=',a
        if a=='1': 
           self.cb_bottom.set_active(True)

        myusers=os.listdir('/home')
        if len(myusers)>0: 
           try:
              myuser=unicode(myusers[0],'utf_8')
           except:
              myuser=unicode(myusers[0],'iso8859_15')
        a=read_entry(self.config,"autologin=","_OFF")
        a=a.replace('\t', ' ')
        a=a.strip()
        print 'autologin=',a
        if a!='_OFF': 
           self.cb_autologin.set_active(True)
           self.entryuser.set_text(a)
        else:
           if len(myusers)>0: self.entryuser.set_text(myuser)


        a=read_entry(self.config,"session=","/usr/bin/startlxde")
        a=a.replace('\t', ' ')
        a=a.strip()
        print 'session=',a
        self.entrysession.set_text(a)
        a=read_entry(self.config,"session=","_OFF")
        if a!='_OFF': self.cb_session.set_active(True)

 
        a=read_entry(self.config,"bg=","/usr/share/wallpapers/default.png")
        a=a.replace('\t', ' ')
        a=a.strip()
        print 'bg=',a
        i=1
        themes=get_themes('/usr/share/wallpapers')
        for theme in themes:
            if theme==a: self.combobox.set_active(i)
            i+=1

        a=read_entry(self.config,"theme=","Industrial")
        a=a.replace('\t', ' ')
        a=a.strip()
        print 'theme=',a
        i=0
        themes=get_lxdm_themes()
        for theme in themes:
            if theme==a: self.comboboxLXDM.set_active(i)
            i+=1

        a=read_entry(self.config,"gtk_theme=","Clearlooks")
        a=a.replace('\t', ' ')
        a=a.strip()
        print 'gtk_theme=',a
        i=0
        themes=get_gtk2_themes()
        for theme in themes:
            if theme==a: self.comboboxGTK.set_active(i)
            i+=1



    def theme_changed(self,data):               #Background picture has changed
        model = self.combobox.get_model()
        index = self.combobox.get_active()
        filename=model[index][0]
        try:
           self.err=0
           bild=gtk.gdk.pixbuf_new_from_file(filename)
           bildvorschau=bild.scale_simple(360,240,gtk.gdk.INTERP_BILINEAR)
           del bild
           self.image.set_from_pixbuf(bildvorschau)
           gc.collect()
        except:
           self.err=1
           self.image.set_from_stock('gtk-stop', gtk.ICON_SIZE_DIALOG)


    def lxdm_theme_changed(self,data):
        if self.err==1:
           try: 
                model = self.comboboxLXDM.get_model()
                index = self.comboboxLXDM.get_active()
                filename='/usr/share/lxdm/themes/' + model[index][0] + '/'
                f=codecs.open(filename + 'gtkrc','r','utf_8')
                text2=f.read()
                f.close()
                text=text2.split('\n')          
                text2='' 
                found=0
                a=len('style "')
                b=len('style "back"')
                for line in text:
                    c=len(line)
                    if c>=a:               
                       if line[0:a]=='style "': 
                          found=0
                    if c>=b:
                       if line[0:b]=='style "back"': 
                          found=1
                    if found==1:
                       if 'file="' in line:
                          text2=line.replace('\t','') 
                          text2=text2.strip()
                          text2=text2[5:].replace('"','')
                bild=gtk.gdk.pixbuf_new_from_file(filename+text2)
                bildvorschau=bild.scale_simple(360,240,gtk.gdk.INTERP_BILINEAR)
                del bild
                self.image.set_from_pixbuf(bildvorschau)
                gc.collect()
           except:
                self.image.set_from_stock('gtk-stop', gtk.ICON_SIZE_DIALOG)
                 


    def __init__(self):
        home=os.getenv('HOME')
        if not home: sys.exit(1)
        home=home+'/.lxdmconf'
        if not os.access(home,os.R_OK):
           f=file(home,'w')
           f.write('x=0\n')
           f.write('y=0\n')
           f.write('width=500\n')
           f.write('height=400\n')
           f.close()
        f=file(home,'r')
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
        window.set_title(_('lxdm Login Configuration'))
        window.set_size_request(400,200)
        window.resize(self.width, self.height)
        window.move(self.pos_x,self.pos_y)

        vbox2=gtk.VBox(False,0)
        self.cb_numlock=gtk.CheckButton(_("Numlock"))
        self.cb_lang=gtk.CheckButton(_("choose Language"))
        self.cb_bottom=gtk.CheckButton(_("Bottom Pane"))
        self.cb_autologin=gtk.CheckButton(_("autologin") + '       ')
        label1=gtk.Label(_("User") + ':')
        label1spacer=gtk.Label("     ")
        self.entryuser=gtk.Entry(max=0)
        hbox2 = gtk.HBox(False, 0)
        hbox2.pack_start(self.cb_autologin,False,False,0)
        hbox2.pack_start(label1,False,False,0)
        hbox2.pack_start(self.entryuser,True,True,0)
        #hbox2.pack_start(label1spacer,False,False,0)
        vbox2.pack_start(self.cb_numlock,False,False,0)
        vbox2.pack_start(self.cb_lang,False,False,0)
        vbox2.pack_start(self.cb_bottom,False,False,0)
        vbox2.pack_start(hbox2,False,False,0)
        hbox3 = gtk.HBox(False, 0)
        self.cb_session=gtk.CheckButton(_("session") + ':')
        labelhspacer=gtk.Label(' ')
        label2spacer=gtk.Label(" ")
        self.entrysession=gtk.Entry(max=0)
        hbox3.pack_start(self.cb_session,False,False,0)
        hbox3.pack_start(self.entrysession,True,True,0)
        #hbox3.pack_start(label2spacer,False,False,0)
        vbox2.set_border_width(20)
        vbox2.pack_start(labelhspacer,True,True,0)
        vbox2.pack_start(hbox3,False,False,0)

        self.image=gtk.Image()
        hbox5 = gtk.HBox(False, 0)
        hbox4 = gtk.HBox(False, 0)
        vbox4 = gtk.VBox(False, 0)
        labeltext=_('Theme')
        label2=gtk.Label(_('Background')+':')
        label12=gtk.Label('  GTK2-'+labeltext+':')
        label13=gtk.Label(labeltext+':')
        self.comboboxGTK = gtk.combo_box_new_text()
        themes=get_gtk2_themes()
        for theme in themes:
            self.comboboxGTK.append_text(theme)
        self.comboboxLXDM = gtk.combo_box_new_text()
        themes=get_lxdm_themes()
        for theme in themes:
            self.comboboxLXDM.append_text(theme)
        self.combobox = gtk.combo_box_new_text()
        self.combobox.connect( 'changed', self.theme_changed)
        self.combobox.append_text(labeltext)
        themes=get_themes('/usr/share/wallpapers')
        for theme in themes:
            self.combobox.append_text(theme)
        self.combobox.set_active(0)
        self.comboboxLXDM.connect( 'changed', self.lxdm_theme_changed)
        hbox5.pack_start(label13,False,False,0)
        hbox5.pack_start(self.comboboxLXDM,True,True,0)
        hbox5.pack_start(label12,False,False,0)
        hbox5.pack_start(self.comboboxGTK,True,True,0)
        hbox4.pack_start(label2,False,False,0)
        hbox4.pack_start(self.combobox,True,True,0)
        vbox4.pack_start(hbox5,False,False,0)
        vbox4.pack_start(hbox4,False,False,0)
        vbox4.pack_start(self.image,True,True,0)
 
        notebook = gtk.Notebook()
        notebook.set_tab_pos(gtk.POS_TOP)
        tab_label1=gtk.Label(_('General'))
        tab_label2=gtk.Label(_('Themes'))
        notebook.append_page(vbox2,tab_label1) 
        notebook.append_page(vbox4,tab_label2) 

        vbox.pack_start(notebook, True, True, 0)

        hbox = gtk.HBox(False, 0)
        button1=gtk.Button(stock='gtk-apply')
        hiddenlabel=gtk.Label(' ')
        button2=gtk.Button(stock='gtk-cancel')
        hbox.pack_start(button1,False,False,0)
        hbox.pack_start(hiddenlabel,True,True,0)
        hbox.pack_start(button2,False,False,0)
        button1.connect_object("clicked", self.save,None)
        button2.connect_object("clicked", self.goodbye,None)
        self.combobox.set_tooltip_text('/usr/share/wallpapers')

        vbox.pack_end(hbox, False, False, 5)
        window.set_border_width(2)
        self.read_config()
        window.show_all()
        userid=os.getuid()
        if userid!=0:
               dialog = gtk.MessageDialog(self.window, gtk.DIALOG_MODAL,gtk.MESSAGE_ERROR,gtk.BUTTONS_OK, "ERROR: not root!")
               result = dialog.run()
               dialog.destroy()
               sys.exit(1)


    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()



# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
     Elfriede = Tool()
     Elfriede.main()

'''
Desactived previous local support
import locale
locale.setlocale(locale.LC_ALL, '')           #set locale from 'LANG'
Xcodec=locale.getpreferredencoding(False)

I18N={}

def i18n(text):
    if I18N_ready:
       if I18N.has_key(text): return I18N[text]
       else: return text
    else: return text

def load_i18n(filename):
     #lÃ¤dt Internationalisierung.moo file
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
     
     codec1=Xcodec.lower().replace('iso-','iso').replace('-','_')
     if 'ansi' in codec1: codec1='iso8859_1'  #Ansi is shit...
     I18N_ready = load_i18n('lxdmconf.moo')
'''

