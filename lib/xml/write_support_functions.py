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
    cdata_string="<![CDATA["+string+"]]>"
    return cdata_string
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def uidstr (guid):
    uid_string=" uid="+"\""+guid+"\""
    return uid_string
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def cidstr (guid):
    uid_string=" cid="+"\""+guid+"\""
    return uid_string
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def pidstr (guid):
    pid_string=" pid="+"\""+guid+"\""
    return pid_string
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def permstr (perm):
    perm_string=" habilitado="+"\""+str(perm)+"\""
    return perm_string
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def qtystr (quantity):
    qty_string=" quantidade="+"\""+str(quantity)+"\""
    return qty_string
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def urlparticipa (prefix, guid):
    http_str="http://participatorio.juventude.gov.br/"
    url_participa=http_str+prefix+guid
    return url_participa
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def hrefstr (url):
    href_string=" href="+"\""+url+"\""
    return href_string
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def datestr (time):
    if time != '':
        date=str(datetime.datetime.fromtimestamp(int(time)))
    else:
        date=''
    return date
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def post_content (db, post_guid, content_typeid):
    content = db.cursor()
    content.execute(qry.qry_post_content, (post_guid, content_typeid,))
    if content.rowcount == 1:
        post_content = content.fetchone()[0]
    else:
        post_content=''
        print "ERRO! Nenhum ou Mais do que um resultado para a query"
        
    content.close()
    
    return post_content
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def postcontent_permission (db, group_guid, content_id):
        
    perm = db.cursor()
    perm.execute(qry.qry_post_content_permission, (group_guid, content_id,))

    if perm.rowcount == 1:
       permission=perm.fetchone()[0]
    else:
        permission=''
        print "ERRO! Nenhum ou Mais do que um resultado para a query"
    
    perm.close()
    
    return permission        
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def groupaccess_permission (db, group_guid):
        
    access = db.cursor()
    
    # 55 = select * from elgg_metastrings where string = 'membership';
    access.execute(qry.qry_group_access_permission, (group_guid, 55,))

    if access.rowcount == 1:
       access_control=access.fetchone()[0]
    else:
        access_control=''
        print "ERRO! Nenhum ou Mais do que um resultado para a query"
    
    access.close()
    
    return access_control        
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