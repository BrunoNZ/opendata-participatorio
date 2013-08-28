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

from users_section_lib import write_users_section 
from groups_section_lib import write_groups_section 

def main():
    
    db = MySQLdb.connect(host='localhost', \
                        user='opendata', \
                        passwd='123mudar', \
                        db='elgg', \
                        charset='utf8')
    
    write_users_section(db,'secao_users.xml')
    write_groups_section(db,'secao_groups.xml')
    
    db.close()   
    
    return 0

if __name__ == '__main__':
    main()

