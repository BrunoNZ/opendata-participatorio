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

import opendata_string_functions as strf
import opendata_queries_definition as qry

class OpendataXML:
    
    database = None
    indentation = None
    level = None
    dir_results = None
    filename = None
    out_file = None
    
    #--------------------------------------------------------------------#    
    def __init__ (self, database, dir_results, filename):
        self.database = database
        
        self.indentation = 0
        self.level = strf.lvl(self.indentation)
        
        self.dir_results = dir_results
        self.filename = filename
    #--------------------------------------------------------------------#

    #--------------------------------------------------------------------#
    def update_indentation(self, increment):
        self.indentation=self.indentation+(increment)
        self.level = strf.lvl(self.indentation)
    #--------------------------------------------------------------------#

    #--------------------------------------------------------------------#
    def open_file (self):
        self.out_file = codecs.open(self.filename,'w',encoding='utf-8')
        self.out_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    #--------------------------------------------------------------------#

    #--------------------------------------------------------------------#
    def close_file (self):
        self.out_file.close()
    #--------------------------------------------------------------------#

    #--------------------------------------------------------------------#
    def write_open_tag (self, tag_name, attr_str):
        self.out_file.write(self.level+"<"+tag_name+attr_str+">"+"\n")
        self.update_indentation(+1)
    #--------------------------------------------------------------------#

    #--------------------------------------------------------------------#
    def write_close_tag (self, tag_name):
        self.update_indentation(-1)
        self.out_file.write(self.level+"</"+tag_name+">"+"\n")
    #--------------------------------------------------------------------#

    #--------------------------------------------------------------------#
    def write_tag (self, tag_name, info_str, attr_str):
        if len(info_str) > 0:
            tag_begin=("<"+tag_name+attr_str+">")
            tag_end=("</"+tag_name+">")
            self.out_file.write(self.level+tag_begin+info_str+tag_end+"\n")
        else:
            self.out_file.write(self.level+"<"+tag_name+attr_str+"/>"+"\n")
    #--------------------------------------------------------------------#

    #--------------------------------------------------------------------#
    def write_comments (self, post_guid):
        post_comments = self.database.cursor()
        post_comments.execute(qry.qry_post_comments, (post_guid,))
                
        self.write_open_tag("comentarios",'')
        for (user_id, user_name, user_username, string, time)\
            in post_comments:
            
            self.write_open_tag("comentario",'')
            
            prefix='profile/'
            user_attr=strf.uidstr(strf.urlparticipa(prefix,user_username))
            self.write_tag("usuario",user_name,user_attr)
            self.write_tag("data",strf.datestr(time),'')
            self.write_tag("mensagem",strf.cdata(string),'')
            
            self.write_close_tag("comentario")
            
        self.write_close_tag("comentarios")
        
        post_comments.close()
    #--------------------------------------------------------------------#
