#!/usr/bin/python
# -*- coding: UTF-8 -*-
#**************************************************************************
#                                                                         *
#   Copyright (c) 2008 by Elfriede Apfelkuchen                            *
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
import pango
display=gtk.gdk.display_get_default()


DefaultIcon=[
"16 16 4 1",
"a c #00ffff",
"# c #000000",
". c None",
"b c #00c0c0",
".......##.......",
"......####......",
".....######.....",
".......##.......",
"....########....",
"..#.#aabbaa#.#..",
".##.#ab##ba#.##.",
"#####a#aa#a#####",
"#####a####a#####",
".##.#a#aa#a#.##.",
"..#.#abaaba#.#..",
"....########....",
".......##.......",
".....######.....",
"......####......",
".......##......."]

irgb=[
"18 6 3 1",
"# c #00ff00",
"a c #0000ff",
". c #ff0000",
"......######aaaaaa",
"......######aaaaaa",
"......######aaaaaa",
"......######aaaaaa",
"......######aaaaaa",
"......######aaaaaa"]

ibgr=[
"18 6 3 1",
"# c #00ff00",
". c #0000ff",
"a c #ff0000",
"......######aaaaaa",
"......######aaaaaa",
"......######aaaaaa",
"......######aaaaaa",
"......######aaaaaa",
"......######aaaaaa"]

ivrgb=[
"12 12 3 1",
"# c #00ff00",
"a c #0000ff",
". c #ff0000",
"............",
"............",
"............",
"............",
"############",
"############",
"############",
"############",
"aaaaaaaaaaaa",
"aaaaaaaaaaaa",
"aaaaaaaaaaaa",
"aaaaaaaaaaaa"]

ivbgr=[
"12 12 3 1",
"# c #00ff00",
". c #0000ff",
"a c #ff0000",
"............",
"............",
"............",
"............",
"############",
"############",
"############",
"############",
"aaaaaaaaaaaa",
"aaaaaaaaaaaa",
"aaaaaaaaaaaa",
"aaaaaaaaaaaa"]

class Simple:

    def destroy(self, widget, data=None):
        #wird beim beenden ausgefÃ¼hrt
        gtk.main_quit()


    def get_string(self):
        #erstellt ein fontconfig configfile als textstring,
        #zuerst GUI-Elemente auswerten...
        index = self.combobox.get_active()
        hintstyle='hintnone'
        if index==1: hintstyle='hintslight'
        if index==2: hintstyle='hintmedium'
        if index==3: hintstyle='hintfull'
        if self.autohint.get_active(): autohint='true'
        else: autohint='false'
        if self.anti.get_active(): anti='true'
        else: anti='false'
        rgba='none'
        if self.radio2.get_active(): rgba='rgb'
        if self.radio3.get_active(): rgba='bgr'
        if self.radio4.get_active(): rgba='vrgb'
        if self.radio5.get_active(): rgba='vbgr'

        #erstellen des fontconfig Strings
        s='<?xml version="1.0"?>\n'
        s+='<!DOCTYPE fontconfig SYSTEM "fonts.dtd">\n'
        s+='<!-- ~/.fonts.conf for per-user font configuration -->\n'
        s+='<fontconfig>\n'
        s+='  <match target="font">\n'
        s+='    <edit name="antialias" mode="assign"><bool>'+anti+'</bool></edit>\n'
        s+='    <edit name="hinting" mode="assign"><bool>true</bool></edit>\n'
        s+='    <edit name="autohint" mode="assign"><bool>'+autohint+'</bool></edit>\n'
        s+='    <edit name="hintstyle" mode="assign"><const>'+hintstyle+'</const></edit>\n'
        s+='    <edit name="rgba" mode="assign"><const>'+rgba+'</const></edit>\n'
        s+='  </match>\n'
        s+='</fontconfig>\n'
        return s


    def save(self,data):
        #wird ausgefÃ¼hrt wenn Anwenden geklickt wird
        text=self.get_string()
        try:
            home=os.getenv("HOME")
            f=open(os.path.join(home,'.fonts.conf'),'w')
            if f:
               f.write(text)
               f.close()
        except:
            print "can't write ~/.fonts.conf"
        print text

        #werte GUI-Elemente aus
        index = self.combobox.get_active()
        hintstyle='hintnone'
        if index==1: hintstyle='hintslight'
        if index==2: hintstyle='hintmedium'
        if index==3: hintstyle='hintfull'
        if self.autohint.get_active(): autohint='1'
        else: autohint='0'
        if self.anti.get_active(): anti='1'
        else: anti='0'
        rgba='none'
        if self.radio2.get_active(): rgba='rgb'
        if self.radio3.get_active(): rgba='bgr'
        if self.radio4.get_active(): rgba='vrgb'
        if self.radio5.get_active(): rgba='vbgr'

        #erstellt den Xft-String fÃ¼r ~/.fonts.sh
        text='#!/bin/sh\n'
        text=text+'echo "Xft.antialias: '+anti+'" | xrdb -merge\n'
        text=text+'echo "Xft.hinting: 1" | xrdb -merge\n'
        text=text+'echo "Xft.autohint: '+autohint+'" | xrdb -merge\n'
        text=text+'echo "Xft.hintstyle: '+hintstyle+'" | xrdb -merge\n'
        text=text+'echo "Xft.rgba: '+rgba+'" | xrdb -merge\n'
        if self.cb_dpi.get_active():
           dpi=str(int(self.adj.get_value()))
           text = text + 'xrandr --dpi ' + dpi
        print '================================================='
        print text
        try:
            home=os.getenv("HOME")
            namen=home+'/.fonts.sh' 
            f=open(namen,'w')
            if f:
               f.write(text)
               f.close()
               os.system('chmod a+x '+namen)
               os.system(namen)
        except:
            print "can't write ~/.fonts.sh"

        #erstellt ~/.config/autostart/fontconfig.desktop damit ~/.fonts.sh (Xft) beim booten ausgefÃ¼hrt wird.
        try:
            os.system('mkdir ~/.config/autostart 2>/dev/null')
            home=os.getenv("HOME")
            namen2=home+'/.config/autostart/fontconfig.desktop' 
            f=open(namen2,'w')
            if f:
              f.write('\n[Desktop Entry]\n')
              f.write('Encoding=UTF-8\n')
              f.write('Version=0.9.4\n')
              f.write('Type=Application\n')
              f.write('Icon=fonts\n')  
              f.write('Name=fontconfig\n')
              f.write('Comment=Antialising,Subpixelrendering\n')
              f.write('Exec='+namen+'\n')
              f.write('StartupNotify=false\n')
              f.write('Terminal=false\n')
              f.write('Hidden=false\n')
              f.close()
        except:
            print "can't write fontconfig.desktop"
        display.beep()
        display.sync()
        gtk.main_quit()


    def goodbye(self,data):
        #Abbrechen wurde angeklickt...
        gtk.main_quit()


    def set_font(self,text):
        #Defaultfont wurde angeklickt, erzeugt jetzt Defaultfont-dialog 
        self.font_dialog=gtk.FontSelectionDialog(_('Select Default Font'))
        self.font_dialog.set_font_name('Sans 10')
        self.font_dialog.set_position(gtk.WIN_POS_MOUSE)
        self.font_dialog.connect("destroy", self.set_font3)
        self.font_dialog.ok_button.connect("clicked",self.set_font2)
        self.font_dialog.cancel_button.connect_object("clicked",lambda wid: wid.destroy(),self.font_dialog)
        if not (self.font_dialog.flags() & gtk.VISIBLE):
           self.font_dialog.show()
        else:
           self.font_dialog.destroy()
           self.font_dialog = None    #font_dialog_destroyed

    def set_font2(self, data):
        #im Defaultfont-dialog wurde OK angeklickt
        myfont = self.font_dialog.get_font_name()
        font_desc = pango.FontDescription(myfont)
        if font_desc:
           self.font.modify_font(font_desc)
        self.font.set_text(myfont)
        print myfont
        self.font_dialog.destroy()
        self.font_dialog = None       #font_dialog_destroyed
        #der Defaultfont wird in ~/.gtkrc-2.0 gespeichert, Themes werden dort nicht aktiviert!
        home=os.getenv("HOME")
        f=open(os.path.join(home,'.gtkrc-2.0'),'w')
        if f:
               f.write('style "user-font"\n')
               f.write('{\n')
               f.write('  font_name="'+myfont+'"\n')
               f.write('}\n')
               f.write('widget_class "*" style "user-font"\n')
               f.write('include "'+home+'/.gtkrc-2.0.mine"\n')
               f.close()

    def set_font3(self, data=None):
        #im Defaultfont-dialog wurde Abbrechen geklickt
        self.font_dialog.destroy()
        self.font_dialog = None       #font_dialog_destroyed


    def toggle_dpi(self,data=None):
        s=self.cb_dpi.get_active()
        if s: self.spinner.set_sensitive(1)
        else: self.spinner.set_sensitive(0)


    def __init__(self):
        # create a new window
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window=window
        window.set_title(_('Fontconfig'))
        vbox = gtk.VBox(False, 5)
        window.add(vbox)
        hbox=gtk.HBox(False,5)
        button=gtk.Button(_("Defaultfont"))
        button.connect('clicked',self.set_font)
        hbox.pack_start(button,False,False,0)
        self.font=gtk.Label('')
        hbox.pack_start(self.font,False,False,0)

        #disabled because there are a Defaultfont chooser in Erscheinungsbild
        #vbox.pack_start(hbox,False,False,0)

        self.anti=gtk.CheckButton(_("Antialising"))
        self.anti.set_active(True)
        vbox.pack_start(self.anti,False,False,0)

        frame = gtk.Frame(_("Hinting"))
        vbox2=gtk.VBox(False,5)
        vbox2.set_border_width(5)
        self.autohint=gtk.CheckButton(_("Automatic hinting"))
        self.autohint.set_tooltip_text(_("Automatic hinting doesn't work good!"))
        #self.autohint.set_active(True)
        vbox2.pack_start(self.autohint,False,False)
        hbox2=gtk.HBox(False,10)
        vbox2.pack_start(hbox2,False,False)
        label=gtk.Label(_("Style")+':')
        hbox2.pack_start(label,False,False)   
        combobox = gtk.combo_box_new_text()
        combobox.append_text(_('none'))
        combobox.append_text(_('slight'))
        combobox.append_text(_('medium'))
        combobox.append_text(_('full'))
        combobox.set_active(3)
        combobox.set_tooltip_text(_("stronger Hinting make fonts sharper"))
        self.combobox=combobox
        hbox2.pack_start(combobox,False,False)   
        frame.add(vbox2)
        vbox.pack_start(frame,False,False)   

        frame = gtk.Frame(_("Sub pixel geometry"))
        vbox3=gtk.VBox(False,5)

        radio=gtk.RadioButton(None,_("none"))
        radio.set_tooltip_text(_("don't split a pixel into 3 subpixels (no color artefacts)"))
        radio.set_active(True)
        self.radio1=radio 
        vbox3.pack_start(radio,False,False)

        window.set_resizable(False)
        hbox=gtk.HBox(False,5)
        image=gtk.Image()
        image.set_from_pixbuf(gtk.gdk.pixbuf_new_from_xpm_data(irgb))
        radio=gtk.RadioButton(self.radio1,_("rgb"))       
        radio.set_tooltip_text(_("split a pixel horizontal into 3 subpixels"))
        self.radio2=radio 
        hbox.pack_start(radio,False,False,0)
        hbox.pack_start(image,False,False,0)
        vbox3.pack_start(hbox,False,False)

        hbox=gtk.HBox(False,5)
        image=gtk.Image()
        image.set_from_pixbuf(gtk.gdk.pixbuf_new_from_xpm_data(ibgr))
        radio=gtk.RadioButton(self.radio1,_("bgr"))
        radio.set_tooltip_text(_("split a pixel horizontal into 3 subpixels"))
        self.radio3=radio 
        hbox.pack_start(radio,False,False,0)
        hbox.pack_start(image,False,False,0)
        vbox3.pack_start(hbox,False,False)

        hbox=gtk.HBox(False,5)
        image=gtk.Image()
        image.set_from_pixbuf(gtk.gdk.pixbuf_new_from_xpm_data(ivrgb))
        radio=gtk.RadioButton(self.radio1,_("vrgb"))
        radio.set_tooltip_text(_("split a pixel vertical into 3 subpixels"))
        self.radio4=radio 
        hbox.pack_start(radio,False,False,0)
        hbox.pack_start(image,False,False,0)
        vbox3.pack_start(hbox,False,False)

        hbox=gtk.HBox(False,5)
        image=gtk.Image()
        image.set_from_pixbuf(gtk.gdk.pixbuf_new_from_xpm_data(ivbgr))
        radio=gtk.RadioButton(self.radio1,_("vbgr"))
        radio.set_tooltip_text(_("split a pixel vertical into 3 subpixels"))
        self.radio5=radio 
        hbox.pack_start(radio,False,False,0)
        hbox.pack_start(image,False,False,0)
        vbox3.pack_start(hbox,False,False)

        frame.add(vbox3)
        vbox.pack_start(frame,False,False)   

        frame = gtk.Frame(_("Screen resolution"))
        vbox4=gtk.VBox(False,5)
        vbox4.set_border_width(5)
        hbox=gtk.HBox(False,5)
        self.cb_dpi=gtk.CheckButton(_("override dpi")+':')
        self.cb_dpi.connect_object("toggled",self.toggle_dpi,None)
        self.adj = gtk.Adjustment(96.0, 50.0, 999.0, 1.0, 10.0, 0.0)
        self.spinner = gtk.SpinButton(self.adj, 0, 0)
        self.spinner.set_sensitive(0)
        hbox.pack_start(self.cb_dpi,False,False,0)
        hbox.pack_start(self.spinner,False,False,0)
        vbox4.pack_start(hbox,False,False,0)
        frame.add(vbox4)
        vbox.pack_start(frame,False,False)   

        frame = gtk.Frame(_("Save"))
        hbox=gtk.HBox(False,5) 
        hbox.set_border_width(5)       
        button1=gtk.Button(stock='gtk-apply')
        button2=gtk.Button(stock='gtk-cancel')
        button1.connect('clicked',self.save)
        button2.connect('clicked',self.goodbye)
        hbox.pack_start(button1,False,False,0)
        hbox.pack_start(button2,False,False,0)
        frame.add(hbox)
        vbox.pack_start(frame,False,False)   

        # Here we connect the "destroy" event to a signal handler.
        # This event occurs when we call gtk_widget_destroy() on the window,
        # or if we return FALSE in the "delete_event" callback.
        window.connect("destroy", self.destroy)
        window.set_border_width(5)
        window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        gtk.window_set_default_icon(gtk.gdk.pixbuf_new_from_xpm_data(DefaultIcon))
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
