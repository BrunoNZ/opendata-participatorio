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

import datetime

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
def date_today():
    return str(datetime.date.today())
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def datestr (time):
    if time != "":
        return str(datetime.datetime.fromtimestamp(int(time)))
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
def substbadc (string):
    string = string.replace('\\','\\\\')
    string = string.replace('"','\\"')
    string = string.replace('\t',' ')
    string = string.replace('\n',' ')
    string = string.replace('\r',' ')
    return string
#--------------------------------------------------------------------#
