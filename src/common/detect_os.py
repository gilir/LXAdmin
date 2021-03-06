#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       
#       Copyright 2010 Julien Lavergne <gilir@ubuntu.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import os
import platform

#Detect Linux distribution
os_detection = platform.dist()

#Detect session
session = os.environ['DESKTOP_SESSION']


# Set configuration location.
if os_detection[0] == 'Ubuntu':
    if session == 'Lubuntu':
        config_lxdm = '/etc/xdg/lubuntu/lxdm/lxdm.conf'
        config_openbox_local = os.path.expanduser("~/.config/openbox/lubuntu-rc.xml")
        command_su = "gksu"
        search_software = "gksu synaptic"
    else:
        config_lxdm = '/etc/xdg/lxdm/default.conf'
        config_openbox_local = os.path.expanduser("~/.config/openbox/lxde-rc.xml")
        command_su = "gksu"
        search_software = "gksu synaptic"
else:
    config_lxdm = '/etc/lxdm/lxdm.conf'
    config_openbox_local = os.path.expanduser("~/.config/openbox/lxde-rc.xml")
    command_su = "su-to-root -X -c"
    search_software = "apt-leo"

def get_lxdm_config():
    return config_lxdm

def get_openbox_config():
    return config_openbox_local

def get_command_su():
    return command_su

def get_search_software():
    return search_software
