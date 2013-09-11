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
import write_support_functions as wrt

######################################################################
# Functions that write on XML file

#-------------------------------------------------------------------#
def write_groupmembers_subsection (db, xml, group_guid):
    group_members = db.cursor()
    group_members.execute(qry.qry_group_members, (group_guid,))
    
    wrt.write_tag(xml,2,"quantidade_membros",str(group_members.rowcount))
                    
    wrt.write_open_tag(xml,2,"membros")
    for (user_id, user_name, user_username) in group_members:
        prefix='profile/'
        user_attr=wrt.uidstr(wrt.urlparticipa(prefix,user_username))
        wrt.write_tag(xml,4,"uid",user_attr)
        wrt.write_tag(xml,3,"usuario",user_name)
    wrt.write_close_tag(xml,2,"membros")
    
    group_members.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_groupfiles_subsection (db, xml, group_guid):
    group_files = db.cursor()
    
    # 1 = select * from elgg_entity_subtypes where subtype='file';
    group_files.execute(qry.qry_group_posts, (group_guid, 1,))
    
    # 50 = select * from elgg_metastrings where string='file_enable';
    perm=wrt.postcontent_permission(db, group_guid, 50)
    
    wrt.write_tag(xml,2,"habilitado",wrt.permstr(perm))
    wrt.write_open_tag(xml,2,"arquivos")
    
    for (post_guid, post_title, post_desc, \
            owner_id, owner_name, owner_username, time)\
        in group_files:
        
        wrt.write_open_tag(xml,3,"arquivo")
        
        prefix='file/download/'
        file_link=wrt.urlparticipa(prefix,str(post_guid))
        
        prefix='file/view/'
        post_attr=wrt.pidstr(wrt.urlparticipa(prefix,str(post_guid)))
        wrt.write_tag(xml,4,"pid",post_attr)

        prefix='profile/'
        owner_attr=wrt.uidstr(wrt.urlparticipa(prefix,owner_username))
        
        wrt.write_tag(xml,4,"uid",owner_attr)
        wrt.write_tag(xml,4,"autor",owner_name)
        wrt.write_tag(xml,4,"titulo",post_title)
        wrt.write_tag(xml,4,"data",wrt.datestr(time))
        wrt.write_tag(xml,4,"link",wrt.hrefstr(file_link))
        wrt.write_tag(xml,4,"descricao",wrt.cdata(post_desc))
                    
        wrt.write_comments(db,xml,post_guid)
        
        wrt.write_close_tag(xml,3,"arquivo")
        
    wrt.write_close_tag(xml,2,"arquivos")
    
    group_files.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_groupforumtopics_subsection (db, xml, group_guid):
    group_forumtopics = db.cursor()
    
    # 7 = select * from elgg_entity_subtypes where subtype='groupforumtopic';
    group_forumtopics.execute(qry.qry_group_posts, (group_guid, 7,))
    
    # 52 = select * from elgg_metastrings where string='forum_enable';
    perm=wrt.postcontent_permission(db, group_guid, 52)
    
    wrt.write_tag(xml,2,"habilitado",wrt.permstr(perm))
    wrt.write_open_tag(xml,2,"debates")
    
    for (post_guid, post_title, post_desc, \
        owner_id, owner_name, owner_username, time)\
        in group_forumtopics:
        
        wrt.write_open_tag(xml,3,"debate")
        
        prefix='discussion/view/'
        post_attr=wrt.pidstr(wrt.urlparticipa(prefix,str(post_guid)))
        wrt.write_tag(xml,4,"pid",post_attr)

        prefix='profile/'
        owner_attr=wrt.uidstr(wrt.urlparticipa(prefix,owner_username))
        
        wrt.write_tag(xml,4,"uid",owner_attr)
        wrt.write_tag(xml,4,"autor",owner_name)
        wrt.write_tag(xml,4,"titulo",post_title)
        wrt.write_tag(xml,4,"data",wrt.datestr(time))
        wrt.write_tag(xml,4,"texto",wrt.cdata(post_desc))
            
        wrt.write_comments(db,xml,post_guid)
        
        wrt.write_close_tag(xml,3,"debate")
        
    wrt.write_close_tag(xml,2,"debates")
    
    group_forumtopics.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_groupbookmarks_subsection (db, xml, group_guid):
    group_bookmarks = db.cursor()
    
    # 13 = select * from elgg_entity_subtypes where subtype='bookmarks';
    group_bookmarks.execute(qry.qry_group_posts, (group_guid, 13,))
    
    # 49 = select * from elgg_metastrings where string='bookmarks_enable';
    perm=wrt.postcontent_permission(db, group_guid, 49)
    
    wrt.write_tag(xml,2,"habilitado",wrt.permstr(perm))
    wrt.write_open_tag(xml,2,"favoritos")
    
    for (post_guid, post_title, post_desc, \
            owner_id, owner_name, owner_username, time)\
        in group_bookmarks:
        
        wrt.write_open_tag(xml,3,"")
        
        # 90 = select * from elgg_metastrings where string='address';
        bookmark_link=wrt.post_content(db,post_guid,90)
        
        prefix='bookmarks/view/'
        post_attr=wrt.pidstr(wrt.urlparticipa(prefix,str(post_guid)))
        wrt.write_tag(xml,4,"pid",post_attr)

        prefix='profile/'
        owner_attr=wrt.uidstr(wrt.urlparticipa(prefix,owner_username))
        
        wrt.write_tag(xml,4,"uid",owner_attr)
        wrt.write_tag(xml,4,"autor",owner_name)
        wrt.write_tag(xml,4,"titulo",post_title)
        wrt.write_tag(xml,4,"data",wrt.datestr(time))
        wrt.write_tag(xml,4,"link",wrt.hrefstr(bookmark_link))
        wrt.write_tag(xml,4,"descricao",wrt.cdata(post_desc))
                            
        wrt.write_comments(db,xml,post_guid)
        
        wrt.write_close_tag(xml,3,"")
    
    wrt.write_close_tag(xml,2,"favoritos")
    
    group_bookmarks.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_grouppages_subsection (db, xml, group_guid):
    group_pages = db.cursor()
    
    # 14 = select * from elgg_entity_subtypes where subtype='page_top';
    group_pages.execute(qry.qry_group_posts, (group_guid, 14,))
    
    # 53 = select * from elgg_metastrings where string='pages_enable';
    perm=wrt.postcontent_permission(db, group_guid, 53)
    
    wrt.write_tag(xml,2,"habilitado",wrt.permstr(perm))
    wrt.write_open_tag(xml,2,"paginas")
    
    for (post_guid, post_title, post_desc,
            owner_id, owner_name, owner_username, time)\
        in group_pages:
        
        wrt.write_open_tag(xml,3,"")
        
        prefix='pages/view/'
        post_attr=wrt.pidstr(wrt.urlparticipa(prefix,str(post_guid)))
        wrt.write_tag(xml,4,"pid",post_attr)

        prefix='profile/'
        owner_attr=wrt.uidstr(wrt.urlparticipa(prefix,owner_username))
        
        wrt.write_tag(xml,4,"uid",owner_attr)
        wrt.write_tag(xml,4,"autor",owner_name)
        wrt.write_tag(xml,4,"titulo",post_title)
        wrt.write_tag(xml,4,"data",wrt.datestr(time))
        wrt.write_tag(xml,4,"texto",wrt.cdata(post_desc))
                    
        wrt.write_comments(db,xml,post_guid)
        
        wrt.write_close_tag(xml,3,"pagina")
        
    wrt.write_close_tag(xml,2,"paginas")
    
    group_pages.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_groupvideos_subsection (db, xml, group_guid):
    group_videos = db.cursor()
    
    # 12 = select * from elgg_entity_subtypes where subtype='videos';
    group_videos.execute(qry.qry_group_posts, (group_guid, 12,))
    
    # 399 = select * from elgg_metastrings where string='videos_enable';
    perm=wrt.postcontent_permission(db, group_guid, 399)
    
    wrt.write_tag(xml,2,"habilitado",wrt.permstr(perm))
    wrt.write_open_tag(xml,2,"videos")
    
    for (post_guid, post_title, post_desc, \
            owner_id, owner_name, owner_username, time)\
        in group_videos:
            
        # 477 = select * from elgg_metastrings where string='video_url';
        video_link=wrt.post_content(db,post_guid, 477)
        
        wrt.write_open_tag(xml,3,"video")
            
        prefix='videos/view/'
        post_attr=wrt.pidstr(wrt.urlparticipa(prefix,str(post_guid)))
        wrt.write_tag(xml,4,"pid",post_attr)
        
        prefix='profile/'
        owner_attr=wrt.uidstr(wrt.urlparticipa(prefix,owner_username))
        
        wrt.write_tag(xml,4,"uid",owner_attr)
        wrt.write_tag(xml,4,"autor",owner_name)
        wrt.write_tag(xml,4,"titulo",post_title)
        wrt.write_tag(xml,4,"data",wrt.datestr(time))
        wrt.write_tag(xml,4,"link",wrt.hrefstr(video_link))
        wrt.write_tag(xml,4,"descricao",wrt.cdata(post_desc))
            
        wrt.write_comments(db,xml,post_guid)
        
        wrt.write_close_tag(xml,3,"video")
        
    wrt.write_close_tag(xml,2,"videos")
    
    group_videos.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_groupevents_subsection (db, xml, group_guid):
    group_events = db.cursor()
    
    # 6 = select * from elgg_entity_subtypes where subtype='calendar_event';
    group_events.execute(qry.qry_group_posts, (group_guid, 6,))
    
    # 54 = select * from elgg_metastrings where string='event_calendar_enable';
    perm=wrt.postcontent_permission(db, group_guid, 54)
    
    wrt.write_tag(xml,2,"habilitado",wrt.permstr(perm))
    wrt.write_open_tag(xml,2,"eventos")
    
    for (post_guid, post_title, post_desc, \
            owner_id, owner_name, owner_username, time)\
        in group_events:
            
        wrt.write_open_tag(xml,3,"")
            
        # 18 = select * from elgg_metastrings where string='venue';
        venue=wrt.post_content(db, post_guid, 18)
        
        # 20 = select * from elgg_metastrings where string='start_date';
        time_start=wrt.post_content(db, post_guid, 20)

        # 22 = select * from elgg_metastrings where string='end_date';
        time_end=wrt.post_content(db, post_guid, 22)
        
        # 26 = select * from elgg_metastrings where string='fees';
        fees=wrt.post_content(db, post_guid, 26)
        
        # 28 = select * from elgg_metastrings where string='contact';
        contact=wrt.post_content(db, post_guid, 28)
        
        # 30 = select * from elgg_metastrings where string='organizer';
        organizer=wrt.post_content(db, post_guid, 30)

        prefix='event_calendar/view/'
        post_attr=wrt.pidstr(wrt.urlparticipa(prefix,str(post_guid)))
        wrt.write_tag(xml,4,"pid",post_attr)
                
        prefix='profile/'
        owner_attr=wrt.uidstr(wrt.urlparticipa(prefix,owner_username))
        
        wrt.write_tag(xml,4,"uid",owner_attr)
        wrt.write_tag(xml,4,"autor",owner_name,)
        wrt.write_tag(xml,4,"titulo",post_title)
        wrt.write_tag(xml,4,"data",wrt.datestr(time))
        wrt.write_tag(xml,4,"organizador",organizer)
        wrt.write_tag(xml,4,"contato",contact)
        wrt.write_tag(xml,4,"endereco",venue)
        wrt.write_tag(xml,4,"data_inicio",wrt.datestr(time_start))
        wrt.write_tag(xml,4,"data_fim",wrt.datestr(time_end))
        wrt.write_tag(xml,4,"taxa_participacao",fees)
        wrt.write_tag(xml,4,"descricao",wrt.cdata(post_desc))
        
        wrt.write_close_tag(xml,3,"evento")
        
        wrt.write_comments(db,xml,post_guid)
    
    wrt.write_close_tag(xml,2,"eventos")
    
    group_events.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_groups_section(db, xml_file):

    xml = codecs.open(xml_file,'w',encoding='utf-8')
    
    xml.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?")

    wrt.write_open_tag(xml,0,"comunidades")
    
    groups_info = db.cursor()
    groups_info.execute(qry.qry_groups_info)
    
    for (guid, title, desc, owner_id, owner_name, owner_username, time)\
        in groups_info:
        
        # 45 = select * from elgg_metastrings where string='briefdescription';
        brief_desc=wrt.post_content(db,guid, 45)
        
        wrt.write_open_tag(xml,1,"")
        
        prefix='groups/profile/'
        group_attr=wrt.cidstr(wrt.urlparticipa(prefix,str(guid)))
        wrt.write_tag(xml,4,"cid",group_attr)

        # Write all group's information
        prefix='profile/'
        owner_attr=wrt.uidstr(wrt.urlparticipa(prefix,owner_username))
        
        wrt.write_tag(xml,2,"uid",owner_attr)
        wrt.write_tag(xml,2,"proprietario",owner_name)
        wrt.write_tag(xml,2,"titulo",title)
        wrt.write_tag(xml,2,"data",wrt.datestr(time))
        wrt.write_tag(xml,2,"descricao",wrt.cdata(desc))
        wrt.write_tag(xml,2,"breve_descricao",wrt.cdata(brief_desc))
                                    
        if wrt.groupaccess_permission(db, guid) == 'public':
            
            # Write a list of group member's name
            write_groupmembers_subsection(db, xml, guid)
        
            # Write a list, and all the info, of all posts made on the group.
            write_groupfiles_subsection(db, xml, guid)
            write_groupforumtopics_subsection(db, xml, guid)
            write_groupbookmarks_subsection(db, xml, guid)
            write_grouppages_subsection(db, xml, guid)
            write_groupvideos_subsection(db, xml, guid)
            write_groupevents_subsection(db, xml, guid)
        
        wrt.write_close_tag(xml,1,"comunidade")
        
    wrt.write_close_tag(xml,0,"comunidades")
    
    groups_info.close()
    
    xml.close()
#--------------------------------------------------------------------#

######################################################################
