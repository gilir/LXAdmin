#!/usr/bin/python
# -*- coding: UTF-8 -*-
#**************************************************************************
#                                                                         *
#   Copyright (c) 2009 by Elfriede Apfelkuchen                            *
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
import string
import time
import codecs
import pygtk
pygtk.require('2.0')
import gtk
import pango
import gc

import lxadmin.defs as defs

from gettext import gettext as _

import gettext

gettext.bindtextdomain('lxadmin', defs.LOCALE_DIR)
gettext.textdomain('lxadmin')
_ = gettext.gettext

sprachen={}
sprachen['al']='Albanian'
sprachen['ar']='Arabic'
sprachen['am']='Armenian'
sprachen['az']='Azerbaijani'
sprachen['by']='Belarusian'
sprachen['be']='Belgian'
sprachen['ben']='Bengali'
sprachen['bs']='Bosnian'
sprachen['br']='Brazilian'
sprachen['bg']='Bulgarian'
sprachen['mm']='Burmese'
sprachen['ca']='Canadian'
#  sprachen['ca_enhanced']='French Canadian'
sprachen['cn']='Chinese'
sprachen['hr']='Croatian'
#  sprachen['hr_US']='Croatian (US)'
sprachen['cz']='Czech'
sprachen['cz_qwerty']='Czech (qwerty)'
sprachen['dk']='Danish'
sprachen['nl']='Dutch'
sprachen['dvorak']='Dvorak'
sprachen['ee']='Estonian'
sprachen['fi']='Finnish'
sprachen['fr']='French'
sprachen['ge']='Georgian'
#  sprachen['ge_la']='Georgian (latin)'
#  sprachen['ge_ru']='Georgian (russian)'
sprachen['de']='German'
sprachen['el']='Greek'
sprachen['guj']='Gujarati'
sprachen['gur']='Gurmukhi'
sprachen['dev']='Hindi'
sprachen['hu']='Hungarian'
#  sprachen['hu_US']='Hungarian (US)'
#  sprachen['hu_qwerty']='Hungarian (qwerty)'
sprachen['is']='Icelandic'
sprachen['iu']='Inuktitut'
sprachen['ir']='Iranian'
sprachen['iq']='Iraq'
sprachen['ie']='Irish'
sprachen['il']='Israeli'
#  sprachen['il_phonetic']='Israeli (phonetic)'
sprachen['it']='Italian'
sprachen['jp']='Japanese'
sprachen['kan']='Kannada'
sprachen['lo']='Lao'
sprachen['la']='Latin America'
sprachen['lt']='Lithuanian'
#  sprachen['lt_std']='Lithuanian azerty standard'
sprachen['lv']='Latvian'
sprachen['mk']='Macedonian'
sprachen['ml']='Malayalam'
sprachen['mt']='Maltese'
# sprachen['mt_us']='Maltese (US layout)'
sprachen['ma']='Morocco'
sprachen['nl']='Netherlands'
sprachen['mn']='Mongolian'
sprachen['no']='Norwegian'
sprachen['ogham']='Ogham'
#  sprachen['ori']='Oriya'
sprachen['pl']='Polish'
#  sprachen['pl2']='Polish (qwertz)'
sprachen['pt']='Portuguese'
sprachen['ro']='Romanian'
sprachen['ru']='Russian'
#  sprachen['ru_yawerty']='Russian (cyrillic phonetic)'
#  sprachen['se_FI']='Northern Saami (Finland)'
#  sprachen['se_NO']='Northern Saami (Norway)'
#  sprachen['se_SE']='Northern Saami (Sweden)'
sprachen['sr']='Serbian'
sprachen['si']='Slovenian'
sprachen['sk']='Slovak'
sprachen['kr']='South Korea'
#  sprachen['sk_qwerty']='Slovak (qwerty)'
sprachen['es']='Spanish'
sprachen['se']='Swedish'
sprachen['ch']='Swiss'
#  sprachen['fr_CH']='Swiss French'
#  sprachen['de_CH']='Swiss German'
sprachen['sy']='Syria'
sprachen['syr']='Syriac'
sprachen['tj']='Tajik'
sprachen['tml']='Tamil'
sprachen['tel']='Telugu'
sprachen['th']='Thai (Kedmanee)'
#  sprachen['th_tis']='Thai (TIS-820.2538)'
#  sprachen['th_pat']='Thai (Pattachote)'
sprachen['tr']='Turkish' 
#  sprachen['tr_f']='Turkish (F)'
sprachen['us']='U.S. English'
sprachen['en_US']='U.S. English w/ ISO9995-3'
sprachen['us_intl']='U.S. English w/ deadkeys'
sprachen['ua']='Ukrainian' 
sprachen['gb']='United Kingdom'
sprachen['vn']='Vietnamese'
#  sprachen['yu']='Yugoslavian'


garnix=[
"2 2 2 1",
"a c None",
"b c #ffffff",
"aa",
"aa"]


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

def melke_xorg(langy):
    #extrahiere keyboard varianten aus xorg fuer die angegebene Sprache
    filename='/usr/share/X11/xkb/symbols/'+langy
    try:
       f=codecs.open(filename,'r','utf_8')
       text=f.read()
       f.close()
    except:
       text=[";standard"]
       return text
    text=text.split('\n')
    key=-1
    variants=[";standard"]
    for line in text:
        if line[0:11]=='xkb_symbols':
           line2=line.split('"')
           oldkey=key
           key=line2[1]
           if oldkey!=-1: variants.append(oldkey)
           continue
        if 'name[Group1]' in line:
           line2=line.split('name[Group1]')
           line3=line2[1].split('"')
           if key!=-1: key=key+';'+line3[1]
    if key!=-1: variants.append(key)  
    return variants


class startmenu:
    def destroy(self, widget, data=None):
        #wird beim beenden ausgeführt, oder Abbrechen wurde angeklickt
        gtk.main_quit()


    def save(self,data=None):
        #Anwenden wurde angeklickt
        Default=self.combobox.get_active_text()
        text=Default[:]
        for i in range(self.anzahl):
            if self.liststore[i][0]==1:
               text2=self.liststore[i][2]
               if text2!=Default:
                  text=text+','+text2
        text+=' -variant '
        for i in range(self.anzahl):          
            if self.liststore[i][2]==Default: break
        if self.liststore[i][2]==Default: text+=self.liststore[i][5]
        for i in range(self.anzahl):
            if self.liststore[i][0]==1:
               text2=self.liststore[i][2]
               if text2!=Default:
                  text=text+','+self.liststore[i][5]

        print "setxkbmap -model pc105 -layout",text
        #Tastaturlayout wird umgeschaltet
        os.system("setxkbmap -model pc105 -layout "+text)
        os.system("lxpanelctl restart")
        home=os.getenv('HOME')
        namen = home + '/.language'
        #save sprache in ~/.language
        f=file(namen,'w')
        if f:
           f.write('%s' % text)
           f.flush()
           f.close()
        #wenn Checkbox aktiviert ist, erzeuge xkeyboard.desktop in ~/.config/autostart
        if self.xkeyboard.get_active():
           os.system ('mkdir ~/.config/autostart 2>/dev/null')
           f=file(home+'/.config/autostart/xkeyboard.desktop','w')
           if f:
              f.write('\n[Desktop Entry]\n')
              f.write('Encoding=UTF-8\n')
              f.write('Version=0.9.4\n')
              f.write('Type=Application\n')
              f.write('Icon=input-keyboard\n')
              f.write('Name=X.org-keyboard-layout\n')
              f.write('Comment=set the language layout for the keyboard\n')
              f.write('Exec=bash -c "setxkbmap -model 105 -layout `cat ~/.language`"\n')
              f.write('StartupNotify=false\n')
              f.write('Terminal=false\n')
              f.write('Hidden=false\n')
              f.close()
        gtk.main_quit()


    def variant_changed(self,data):
        #Die keyboardvariante in der combobox wurde geändert
        if self.lock: return
        try:
           model = self.variant.get_model()
           index = self.variant.get_active()
           variant=model[index][0]
        except:
           return
        text=variant.split(';')
        if self.active_language!=-1:
           self.liststore[self.active_language][5]=text[0]


    def row_activate(self, treeview, path, column):
        #Doppelklick auf eine Sprache, aktualisiere default combobox mit Sprachen
        name=self.liststore[path][2]
        state=self.liststore[path][0]
        if state==1:                          #Sprache wird entfernt
           self.liststore[path][0]=0
           self.liststore[path][1]=Soff
           print name,"= 0"
           for i in range(self.comboanzahl): self.combobox.remove_text(0)
           self.comboanzahl=0
           for i in range(self.anzahl):
               if self.liststore[i][0]==1:
                  self.comboanzahl+=1
                  self.combobox.append_text(self.liststore[i][2])
           self.combobox.set_active(0)
        else:                                 #Sprache wird hinzugefügt
           self.liststore[path][0]=1
           self.liststore[path][1]=Son
           print name,"= 1"
           for i in range(self.comboanzahl): self.combobox.remove_text(0)
           self.comboanzahl=0
           for i in range(self.anzahl):
               if self.liststore[i][0]==1:
                  self.comboanzahl+=1
                  self.combobox.append_text(self.liststore[i][2])
           self.combobox.set_active(0)
        gc.collect()


    def mouse(self, widget, event, data=None):
        if event.button==1:
           #eine Sprache wurde angeklickt, setze Variant combobox
           pathinfo=self.treeview.get_path_at_pos(int(event.x),int(event.y)) 
           if pathinfo==None: return False
           pathnr=pathinfo[0][0]  
           name=self.liststore[pathnr][2]
           self.lock=True
           self.active_language=pathnr
           for i in range(self.variantanzahl): self.variant.remove_text(0)
           self.variantanzahl=0
           variants=melke_xorg(name)
           for line in variants: 
               self.variant.append_text(line)
               self.variantanzahl+=1
           self.lock=False


    def __init__(self):
        home=os.getenv('HOME')
        lang=os.getenv('LANG')
        lang=lang[0:2]
        namen = home + '/.language'
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window=window
        window.set_border_width(5)
        window.set_title(_('DoubleClick Language'))
        window.set_size_request(600,400)
        vbox = gtk.VBox(False, 5)
        window.add(vbox)
        window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.liststore=gtk.ListStore(int,gtk.gdk.Pixbuf,str,str,gtk.gdk.Pixbuf,str)
        self.treeview=gtk.TreeView()
        self.treeview.set_headers_visible(True)
        self.treeview.set_model(self.liststore)
        self.treeview.connect('row-activated', self.row_activate)
        self.treeview.set_events(self.treeview.get_events() | gtk.gdk.BUTTON_PRESS_MASK)
        self.treeview.connect("button-press-event", self.mouse)

        self.cellpb = gtk.CellRendererPixbuf()
        self.cell1 = gtk.CellRendererText()
        self.cellf = gtk.CellRendererPixbuf()
        self.cell2 = gtk.CellRendererText()
        self.cellv = gtk.CellRendererText()
        self.cellpb.set_property('cell-background','grey80')
        self.cellf.set_property('cell-background', 'grey80')
        self.cell1.set_property('cell-background', 'grey80')
        self.spalte1 = gtk.TreeViewColumn(_('Language'))
        self.spalte2 = gtk.TreeViewColumn(_('Description'))
        self.spalte3 = gtk.TreeViewColumn(_('Variant'))
        self.treeview.append_column(self.spalte1)
        self.treeview.append_column(self.spalte2)
        self.treeview.append_column(self.spalte3)
        self.spalte1.pack_start(self.cellpb,False)
        self.spalte1.pack_start(self.cell1,True)
        self.spalte1.pack_start(self.cellf,False)
        self.spalte2.pack_start(self.cell2,True)
        self.spalte3.pack_start(self.cellv,True)
        self.spalte1.set_attributes(self.cellpb, pixbuf=1)
        self.spalte1.set_attributes(self.cell1, text=2)
        self.spalte1.set_attributes(self.cellf, pixbuf=4)
        self.spalte2.set_attributes(self.cell2, text=3)
        self.spalte3.set_attributes(self.cellv, text=5)


        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.add(self.treeview)
        self.xkeyboard=gtk.CheckButton(_("install service:  ~/.config/autostart/xkeyboard"))
        self.xkeyboard.set_active(True)
        #vbox.pack_start(self.xkeyboard , False,False, 0)
        vbox.pack_start(sw , True, True, 0)
        window.connect("destroy", self.destroy)

        hbox=gtk.HBox(False,10)
        hbox2=gtk.HBox(False,10)
        label4=gtk.Label(_("Default:"))
        self.combobox = gtk.combo_box_new_text()
        label5=gtk.Label(_("Variant:"))
        self.variant = gtk.combo_box_new_text()
        self.variant.connect('changed', self.variant_changed)
        button1=gtk.Button(stock='gtk-apply')
        button2=gtk.Button(stock='gtk-cancel')
        hbox.pack_start(button1,False,False,0)
        hbox.pack_start(label4,False,False,0)
        hbox.pack_start(self.combobox,True,True, 0)
        hbox2.pack_start(label5,False,False,0)
        hbox2.pack_start(self.variant,True,True, 0)
        hbox.pack_start(button2,False,False,0)
        button1.connect('clicked',self.save)
        button2.connect('clicked',self.destroy)
        vbox.pack_start(hbox2 , False,False, 0)
        vbox.pack_start(hbox , False,False, 0)
        window.show_all()

        try:
             f=file(namen,'r')
             layout0=f.read()
             f.close()
             layout0=layout0.replace('\n','')
             layout1=layout0.split(' ')
             layout=layout1[0].split(',')
             if " -variant " in layout0:
                layout2=layout0.split('-variant ')
                vari=layout2[1].split(',')
             else: vari=['','','','','','','','','','','','','','','','','','','','','']
        except:         
             layout=[ lang[0:2] ]
             vari=['','','','']

        self.lock=True
        self.active_language=-1
        self.variantanzahl=0
        self.comboanzahl=0
        for i in layout:
            self.combobox.append_text(i)
            self.comboanzahl+=1
        self.combobox.set_active(0)

        self.anzahl=len(sprachen.keys())
        
        for i in sprachen.keys():
            try:
               filename='/usr/share/sidux-lxde-common/Flaggen/'+i+'.png'  
               flag=gtk.gdk.pixbuf_new_from_file(filename)
            except:
               flag=Snix
            if flag==Snix:
               try:
                   filename='/usr/share/lxpanel/images/xkb-flags/'+i+'.png' 
                   flag2=gtk.gdk.pixbuf_new_from_file(filename)
                   flag=flag2.scale_simple(26,18,gtk.gdk.INTERP_HYPER)
               except:
                   flag=Snix

            if i in layout:
               for t in range(len(layout)):
                   if layout[t]==i: break
               try: 
                  if layout[t]==i: myvariant=vari[t]
                  else: myvariant=""
               except:
                  myvariant=""
               self.liststore.append([1,Son,i,sprachen[i],flag,myvariant])
            else:
               self.liststore.append([0,Soff,i,sprachen[i],flag,''])

        self.liststore.set_sort_column_id(3, gtk.SORT_ASCENDING)


    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()



# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
     Snix=gtk.gdk.pixbuf_new_from_xpm_data(garnix)
     Soff=gtk.gdk.pixbuf_new_from_xpm_data(rot)
     Son=gtk.gdk.pixbuf_new_from_xpm_data(gruen)
     app=startmenu()
     app.main()
