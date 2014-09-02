#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2004-2008 Centro de Computacao Cientifica e Software Livre
# Departamento de Informatica - Universidade Federal do Parana - C3SL/UFPR
#
# This file is part of participatorio/opendata
#
# participatorio/opendata is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301,
# USA.

import MySQLdb
import datetime

from lib.xml_user_section import write_singlefile_users_section
from lib.xml_group_section import write_singlefile_groups_section

from lib.xml_user_section import write_multifile_users_section
from lib.xml_group_section import write_multifile_groups_section

def main():
    
    # Open connection to database
    db = MySQLdb.connect(host='localhost', \
                        user='opendata', \
                        passwd='123mudar', \
                        db='elgg', \
                        charset='utf8')
    
    # Define directory and name of XML files
    dir_results="/var/www/elgg/opendata_xmlfiles/"
       
    # Get the execution start time information
    time_script_start=datetime.datetime.now()
    
    # Call functions to write Single Dump XML file
    write_singlefile_users_section(db,dir_results)
    write_singlefile_groups_section(db,dir_results)
    
    # Call functions to write Multiple Dump XML files
    #write_multifile_users_section(db,dir_results)
    #write_multifile_groups_section(db,dir_results)
    
    # Calculate and Print script time duration
    script_duration=datetime.datetime.now()-time_script_start
    total_exec_time=str(script_duration.total_seconds())
    print "TOTAL EXECUTION TIME: "+total_exec_time+"\n"
    
    # Close database connection
    db.close()   
    
    return 0

if __name__ == '__main__':
    main()

