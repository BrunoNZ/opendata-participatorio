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

import opendata_string_functions as strf
import opendata_queries_definition as qry

class OpendataJSON:

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
        self.out_file=codecs.open(self.filename,'w',encoding='utf-8')
    #--------------------------------------------------------------------#

    #--------------------------------------------------------------------#
    def close_file (self):
        self.out_file.close()
    #--------------------------------------------------------------------#

    #--------------------------------------------------------------------#
    def write_open_tag (self, tag_name, sep):
        if len(tag_name) > 0:
            self.out_file.write(self.level+"\""+tag_name+"\""+":"+sep+"\n")
        else:
            self.out_file.write(self.level+sep+"\n")
        self.update_indentation(+1)
    #--------------------------------------------------------------------#

    #--------------------------------------------------------------------#
    def write_close_tag (self, sep, comma_flag):
        self.update_indentation(-1)
        if comma_flag == True:
            self.out_file.write(self.level+sep+","+"\n")
        else:
            self.out_file.write(self.level+sep+"\n")
    #--------------------------------------------------------------------#

    #--------------------------------------------------------------------#
    def write_tag (self, tag_name, info_str, comma):
        name="\""+tag_name+"\""
        info="\""+strf.substbadc(info_str)+"\""
        self.out_file.write(self.level+name+":"+info+comma+"\n")
    #--------------------------------------------------------------------#

    #--------------------------------------------------------------------#
    def write_comments (self, post_guid):
        post_comments = self.database.cursor()
        post_comments.execute(qry.qry_post_comments, (post_guid,))
        
        self.write_open_tag("comentarios","[")
        
        row=0
        for (user_id, user_name, user_username, string, time)\
            in post_comments:
            
            row=row+1
            
            self.write_open_tag("","{")
            
            prefix='profile/'
            user_attr=strf.urlparticipa(prefix,user_username)
                    
            self.write_open_tag("usuario","{")
            self.write_tag("uid",user_attr,",")
            self.write_tag("nome",user_name,"")
            self.write_close_tag("}",True)
            
            self.write_tag("data",strf.datestr(time),",")
            self.write_tag("mensagem",string,"")
            
            self.write_close_tag("}",(row < post_comments.rowcount))
            
        self.write_close_tag("]",False)
        
        post_comments.close()
    #--------------------------------------------------------------------#
