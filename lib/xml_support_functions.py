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

import string_functions as strf
import queries_definition as qry

######################################################################
# Support functions:

#--------------------------------------------------------------------#
def open_xml_file (xml_filename):
    xml_file = codecs.open(xml_filename,'w',encoding='utf-8')
    xml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    return xml_file
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_open_tag (xml, l, tag_name, attr_str):
    xml.write(strf.lvl(l)+"<"+tag_name+attr_str+">"+"\n")
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_close_tag (xml, l, tag_name):
    xml.write(strf.lvl(l)+"</"+tag_name+">"+"\n")
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_tag (xml, l, tag_name, info_str, attr_str):
    if len(info_str) > 0:
        tag_begin=("<"+tag_name+attr_str+">")
        tag_end=("</"+tag_name+">")
        xml.write(strf.lvl(l)+tag_begin+info_str+tag_end+"\n")
    else:
        xml.write(strf.lvl(l)+"<"+tag_name+attr_str+"/>"+"\n")
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_comments (db, xml, post_guid):
    post_comments = db.cursor()
    post_comments.execute(qry.qry_post_comments, (post_guid,))
            
    write_open_tag(xml,4,"comentarios",'')
    for (user_id, user_name, user_username, string, time) in post_comments:
        
        write_open_tag(xml,5,"comentario",'')
        
        prefix='profile/'
        user_attr=strf.uidstr(strf.urlparticipa(prefix,user_username))
        write_tag(xml,6,"usuario",user_name,user_attr)
        write_tag(xml,6,"data",strf.datestr(time),'')
        write_tag(xml,6,"mensagem",strf.cdata(string),'')
        
        write_close_tag(xml,5,"comentario")
        
    write_close_tag(xml,4,"comentarios")
    
    post_comments.close()
#--------------------------------------------------------------------#

######################################################################
