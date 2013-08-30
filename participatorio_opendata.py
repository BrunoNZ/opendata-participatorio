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

from lib_user_section import write_users_section 
from lib_group_section import write_groups_section 

def main():
    
    # Open connection to database
    db = MySQLdb.connect(host='localhost', \
                        user='opendata', \
                        passwd='123mudar', \
                        db='elgg', \
                        charset='utf8')
    
    # Define directory and name of XML files
    date_today=str(datetime.date.today())
    dir_results="/root/workdir_bnz07/xml_files/"
    user_xml_file=dir_results+"usuarios_"+date_today+".xml"
    group_xml_file=dir_results+"comunidades_"+date_today+".xml"
    
    # Get the execution start time information
    time_script_start=datetime.datetime.now()
    
    # Call functions to write XML files
    write_users_section(db,user_xml_file)
    write_groups_section(db,group_xml_file)
    
    # Calculate and Print script time duration
    script_duration=datetime.datetime.now()-time_script_start
    total_exec_time=str(script_duration.total_seconds())
    print "TOTAL EXECUTION TIME: "+total_exec_time+"\n"
    
    # Close database connection
    db.close()   
    
    return 0

if __name__ == '__main__':
    main()

