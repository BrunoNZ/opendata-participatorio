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
import codecs
import datetime
import base64

import string_functions as strf
import queries_definition as qry

######################################################################
# Support functions:

#--------------------------------------------------------------------#
def open_json_file (json_filename):
    json_file = codecs.open(json_filename,'w',encoding='utf-8')
    return json_file
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_open_tag (xml, l, tag_name, sep):
    if len(tag_name) > 0:
        xml.write(strf.lvl(l)+"\""+tag_name+"\""+":"+sep+"\n")
    else:
        xml.write(strf.lvl(l)+sep+"\n")
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_close_tag (xml, l, sep, comma_flag):
    if comma_flag == True:
        xml.write(strf.lvl(l)+sep+","+"\n")
    else:
        xml.write(strf.lvl(l)+sep+"\n")    
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_tag (xml, l, tag_name, info_str, comma):
    name="\""+tag_name+"\""
    info="\""+strf.substbadc(info_str)+"\""
    xml.write(strf.lvl(l)+name+":"+info+comma+"\n")
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_comments (db, xml, post_guid):
    post_comments = db.cursor()
    post_comments.execute(qry.qry_post_comments, (post_guid,))
    
    write_open_tag(xml,4,"comentarios","[")
    
    row=0
    for (user_id, user_name, user_username, string, time)\
        in post_comments:
        
        row=row+1
        
        write_open_tag(xml,5,"","{")
        
        prefix='profile/'
        user_attr=strf.urlparticipa(prefix,user_username)
                
        write_open_tag(xml,6,"usuario","{")
        write_tag(xml,7,"uid",user_attr,",")
        write_tag(xml,7,"nome",user_name,"")
        write_close_tag(xml,6,"}",True)
        
        write_tag(xml,6,"data",strf.datestr(time),",")
        write_tag(xml,6,"mensagem",string,"")
        
        write_close_tag(xml,5,"}",(row < post_comments.rowcount))
        
    write_close_tag(xml,4,"]",False)
    
    post_comments.close()
#--------------------------------------------------------------------#

######################################################################
