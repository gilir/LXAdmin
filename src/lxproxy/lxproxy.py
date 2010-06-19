#!/usr/bin/python
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
from user import home

# Check if we are working in the source tree or from the installed 
# package and mangle the python path accordingly
if os.path.dirname(sys.argv[0]) != ".":
    if sys.argv[0][0] == "/":
        fullPath = os.path.dirname(sys.argv[0])
    else:
        fullPath = os.getcwd() + "/" + os.path.dirname(sys.argv[0])
else:
    fullPath = os.getcwd()
sys.path.insert(0, os.path.dirname(fullPath))
DEFAULTDICT = {"export http_proxy": "http://user:password@hostname:8080",
               "export https_proxy": "http://user:password@hostname:8080",
               "export ftp_proxy": "http://user:password@hostname:8080"}

import AboutLxproxyDialog
from lxproxyconfig import getdatapath

class LxproxyWindow(gtk.Window):
    __gtype_name__ = "LxproxyWindow"

    def __init__(self):
        """__init__ - This function is typically not called directly.
        Creation a LxproxyWindow requires redeading the associated ui
        file and parsing the ui definition extrenally,
        and then calling LxproxyWindow.finish_initializing().

        Use the convenience function NewLxproxyWindow to create
        LxproxyWindow object.

        """
        pass

    def finish_initializing(self, builder):
        """finish_initalizing should be called after parsing the ui definition
        and creating a LxproxyWindow object with it in order to finish
        initializing the start of the new LxproxyWindow instance.

        """
        #get a reference to the builder and set up the signals
        self.builder = builder
        self.builder.connect_signals(self)
        global httptxt, httpstxt, ftptxt, sockstxt, httpspin, httpsspin, ftpspin, socksspin,directradio,manualradio
        directradio = self.builder.get_object("directradio")
        manualradio = self.builder.get_object("manualradio")
        httptxt = self.builder.get_object("httptxt")
        httpstxt = self.builder.get_object("httpstxt")
        ftptxt = self.builder.get_object("ftptxt")
        sockstxt = self.builder.get_object("sockstxt")
        httpspin = self.builder.get_object("httpspin")
        httpsspin = self.builder.get_object("httpsspin")
        ftpspin = self.builder.get_object("ftpspin")
        socksspin = self.builder.get_object("socksspin")
        socksbox = self.builder.get_object("hbox4")
        socksbox.hide()
        if manualradio.get_active():
            httptxt.set_sensitive(True)
            httpstxt.set_sensitive(True)
            ftptxt.set_sensitive(True)
            sockstxt.set_sensitive(True)
            httpspin.set_sensitive(True)
            httpsspin.set_sensitive(True)
            ftpspin.set_sensitive(True)
            socksspin.set_sensitive(True)
        else: 
            httptxt.set_sensitive(False)
            httpstxt.set_sensitive(False)
            ftptxt.set_sensitive(False)
            sockstxt.set_sensitive(False)
            httpspin.set_sensitive(False)
            httpsspin.set_sensitive(False)
            ftpspin.set_sensitive(False)
            socksspin.set_sensitive(False)
        httpspin.set_value(8080)
        httpsspin.set_value(8080)
        ftpspin.set_value(8080)
        socksspin.set_value(8080)

        self.readfile()

        #uncomment the following code to read in preferences at start up
        #dlg = PreferencesLxproxyDialog.NewPreferencesLxproxyDialog()
        #self.preferences = dlg.get_preferences()

        #code for other initialization actions should be added here

    def readfile(self):
        profile_location = os.path.expanduser('~/.profile')
        if not os.path.exists(profile_location):
            tmpfile = open(profile_location, 'w') 
            tmpfile.write('') 
            tmpfile.close()
        try:
            data = profile_location.read()
            profile_location.close()
            config = self.parse(data)
        except:
            print "Could not open proxyconfig"

    def parse(self, s):
        #Fetch a *copy* of the default dictionary.
        ret = DEFAULTDICT.copy()
        # Split lines
        lines = s.split("\n")
        for line in lines:
            line = line.strip()
            #if line and line[0] != "#":
            if line.startswith('export'):
                manualradio.set_active(True)
                values = line.split("=")
                ret[values[0]] = values[1]

        try:
            #print ret # Debugging
            port=ret["export http_proxy"].split(":")
            httptxt.set_text(port[0]+":"+port[1]+":"+port[2])
            httpspin.set_value(float(port[3]))
            port=ret["export https_proxy"].split(":")
            httpstxt.set_text(port[0]+":"+port[1]+":"+port[2])
            httpsspin.set_value(float(port[3]))
            port=ret["export ftp_proxy"].split(":")
            ftptxt.set_text(port[0]+":"+port[1]+":"+port[2])
            ftpspin.set_value(float(port[3]))
        except:
            try:
                port=ret["export http_proxy"].split(":")
                httptxt.set_text(port[0]+":"+port[1])
                httpspin.set_value(float(port[2]))
                port=ret["export https_proxy"].split(":")
                httpstxt.set_text(port[0]+":"+port[1])
                httpsspin.set_value(float(port[2]))
                port=ret["export ftp_proxy"].split(":")
                ftptxt.set_text(port[0]+":"+port[1])
                ftpspin.set_value(float(port[2]))
            except:    
                httptxt.set_text(ret["export http_proxy"])
                httpstxt.set_text(ret["export https_proxy"])
                ftptxt.set_text(ret["export ftp_proxy"])


    def on_closebtn_clicked(self,widget):
        if directradio.get_active():
           file(home+'/.profile2', 'w').writelines([l for l in file(home+'/.profile').readlines() if 'export http_proxy' not in l]) 
           os.system("mv "+ home+"/.profile2 " + home + "/.profile")
           file(home+'/.profile2', 'w').writelines([l for l in file(home+'/.profile').readlines() if 'export https_proxy' not in l]) 
           os.system("mv "+ home+"/.profile2 " + home + "/.profile")
           file(home+'/.profile2', 'w').writelines([l for l in file(home+'/.profile').readlines() if 'export ftp_proxy' not in l]) 
           os.system("mv "+ home+"/.profile2 " + home + "/.profile")
           file(home+'/.profile2', 'w').writelines([l for l in file(home+'/.profile').readlines() if 'export HTTP_PROXY' not in l]) 
           os.system("mv "+ home+"/.profile2 " + home + "/.profile")
           file(home+'/.profile2', 'w').writelines([l for l in file(home+'/.profile').readlines() if 'export HTTPS_PROXY' not in l]) 
           os.system("mv "+ home+"/.profile2 " + home + "/.profile")
           file(home+'/.profile2', 'w').writelines([l for l in file(home+'/.profile').readlines() if 'export FTP_PROXY' not in l]) 
           os.system("mv "+ home+"/.profile2 " + home + "/.profile")
        else:
            os.system("echo 'export http_proxy="+httptxt.get_text()+":"+str(httpspin.get_value())[:-2]+"' >> "+ home+ "/.profile")
            os.system("echo 'export https_proxy="+httpstxt.get_text()+":"+str(httpsspin.get_value())[:-2]+"' >> "+ home+ "/.profile")
            os.system("echo 'export ftp_proxy="+ftptxt.get_text()+":"+str(ftpspin.get_value())[:-2]+"' >> "+ home+ "/.profile")
            os.system("echo 'export HTTP_PROXY=$http_proxy' >> "+ home+ "/.profile")
            os.system("echo 'export HTTPS_PROXY=$https_proxy' >> "+ home+ "/.profile")
            os.system("echo 'export FTP_PROXY=$ftp_proxy' >> "+ home+ "/.profile")
        self.quit(self,widget)

    def on_manualradio_toggled(self,widget):
        httptxt.set_sensitive(True)
        httpstxt.set_sensitive(True)
        ftptxt.set_sensitive(True)
        sockstxt.set_sensitive(True)
        httpspin.set_sensitive(True)
        httpsspin.set_sensitive(True)
        ftpspin.set_sensitive(True)
        socksspin.set_sensitive(True)

    def on_directradio_toggled(self,widget):
        httptxt.set_sensitive(False)
        httpstxt.set_sensitive(False)
        ftptxt.set_sensitive(False)
        sockstxt.set_sensitive(False)
        httpspin.set_sensitive(False)
        httpsspin.set_sensitive(False)
        ftpspin.set_sensitive(False)
        socksspin.set_sensitive(False)
        

    def about(self, widget, data=None):
        """about - display the about box for lxproxy """
        about = AboutLxproxyDialog.NewAboutLxproxyDialog()
        response = about.run()
        about.destroy()

    def preferences(self, widget, data=None):
        """preferences - display the preferences window for lxproxy """
        prefs = PreferencesLxproxyDialog.NewPreferencesLxproxyDialog()
        response = prefs.run()
        if response == gtk.RESPONSE_OK:
            #make any updates based on changed preferences here
            pass
        prefs.destroy()

    def quit(self, widget, data=None):
        """quit - signal handler for closing the LxproxyWindow"""
        self.destroy()

    def on_destroy(self, widget, data=None):
        """on_destroy - called when the LxproxyWindow is close. """
        #clean up code for saving application state should be added here

        gtk.main_quit()

def NewLxproxyWindow():
    """NewLxproxyWindow - returns a fully instantiated
    LxproxyWindow object. Use this function rather than
    creating a LxproxyWindow directly.
    """

    #look for the ui file that describes the ui
    ui_filename = os.path.join(getdatapath(), 'ui', 'lxproxy', 'LxproxyWindow.ui')
    if not os.path.exists(ui_filename):
        ui_filename = None

    print ('1',ui_filename)
    builder = gtk.Builder()
    builder.add_from_file(ui_filename)
    window = builder.get_object("lxproxy_window")
    window.finish_initializing(builder)
    return window

if __name__ == "__main__":
    #support for command line options
    import logging, optparse
    parser = optparse.OptionParser(version="%prog %ver")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="Show debug messages")
    (options, args) = parser.parse_args()

    #set the logging level to show debug messages
    if options.verbose:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug('logging enabled')

    #run the application
    window = NewLxproxyWindow()
    window.show()
    gtk.main()

