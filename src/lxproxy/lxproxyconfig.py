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

# THIS IS Lxproxy CONFIGURATION FILE
# YOU CAN PUT THERE SOME GLOBAL VALUE
# Do not touch until you know what you're doing.
# you're warned :)

# where your project will head for your data (for instance, images and ui files)
# by default, this is ../data, relative your trunk layout
__lxproxy_data_directory__ = '../../data/'


import os

import lxadmin.defs as defs

class project_path_not_found(Exception):
    pass

def getdatapath(ui):
    """Retrieve lxproxy data path

    This path is by default <lxproxy_lib_path>/../data/ in trunk
    and /usr/share/lxproxy in an installed version but this path
    is specified at installation time.
    """
    
    ui_path = os.path.join(os.getcwd(),ui)
    if not os.path.exists(ui_path):
        ui_path = os.path.join(defs.SHARED_DATA_DIR,"lxproxy",ui)
    return ui_path

    # get pathname absolute or relative
    #if __lxproxy_data_directory__.startswith('/'):
    #    pathname = __lxproxy_data_directory__
    #else:
    #    pathname = os.path.dirname(__file__) + '/' + __lxproxy_data_directory__

    #abs_data_path = os.path.abspath(pathname)
    #if os.path.exists(abs_data_path):
    #    return abs_data_path
    #else:
    #    raise project_path_not_found

