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
def date_today():
    return str(datetime.date.today())
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def lvl (l):
    if l == 1:
        return "\t"
    elif l == 2:
        return "\t\t"
    elif l == 3:
        return "\t\t\t"
    elif l == 4:
        return "\t\t\t\t"
    elif l == 5:
        return "\t\t\t\t\t"
    elif l == 6:
        return "\t\t\t\t\t\t"
    elif l == 7:
        return "\t\t\t\t\t\t\t"
    else:
        return ""
#--------------------------------------------------------------------#    

#--------------------------------------------------------------------#
def cdata (string):
    if len(string) > 0:
        return "<![CDATA["+string+"]]>"
    else:
        return ""
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def uidstr (guid):
    return " uid="+"\""+guid+"\""
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def cidstr (guid):
    return " cid="+"\""+guid+"\""
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def pidstr (guid):
    return " pid="+"\""+guid+"\""
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def permstr (perm):
    return " habilitado="+"\""+str(perm)+"\""
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def qtystr (quantity):
    return " quantidade="+"\""+str(quantity)+"\""
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def urlparticipa (prefix, guid):
    return "http://participatorio.juventude.gov.br/"+prefix+guid
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def hrefstr (url):
    return " href="+"\""+url+"\""
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def datestr (time):
    if time != "":
        return str(datetime.datetime.fromtimestamp(int(time)))
    else:
        return ""
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_open_tag (xml, l, tag_name, attr_str):
    xml.write(lvl(l)+"<"+tag_name+attr_str+">"+"\n")
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_close_tag (xml, l, tag_name):
    xml.write(lvl(l)+"</"+tag_name+">"+"\n")
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_tag (xml, l, tag_name, info_str, attr_str):
    level=lvl(l)
    if len(info_str) > 0:
        tag_begin=("<"+tag_name+attr_str+">")
        tag_end=("</"+tag_name+">")
        xml.write(level+tag_begin+info_str+tag_end+"\n")
    else:
        xml.write(level+"<"+tag_name+attr_str+"/>"+"\n")
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_comments (db, xml, post_guid):
    post_comments = db.cursor()
    post_comments.execute(qry.qry_post_comments, (post_guid,))
            
    write_open_tag(xml,4,"comentarios",'')
    for (user_id, user_name, user_username, string, time) in post_comments:
        
        write_open_tag(xml,5,"comentario",'')
        
        prefix='profile/'
        user_attr=uidstr(urlparticipa(prefix,user_username))
        write_tag(xml,6,"usuario",user_name,user_attr)
        write_tag(xml,6,"data",datestr(time),'')
        write_tag(xml,6,"mensagem",cdata(string),'')
        
        write_close_tag(xml,5,"comentario")
        
    write_close_tag(xml,4,"comentarios")
    
    post_comments.close()
#--------------------------------------------------------------------#

######################################################################
