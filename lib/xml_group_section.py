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

from opendata_xml_class import OpendataXML

import opendata_queries_definition as qry
import opendata_string_functions as strf

######################################################################
# Functions that write on XML file

#-------------------------------------------------------------------#
def write_groupmembers_subsection (xml, group_guid):
    group_members = xml.database.cursor()
    group_members.execute(qry.qry_group_members, (group_guid,))
    
    qty=str(group_members.rowcount)
    xml.write_tag("quantidade_membros",qty,'')
                    
    xml.write_open_tag("membros",'')
    for (user_id, user_name, user_username) in group_members:
        prefix='profile/'
        user_attr=strf.uidstr(strf.urlparticipa(prefix,user_username))
        xml.write_tag("usuario",user_name,user_attr)
    xml.write_close_tag("membros")
    
    group_members.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_groupfiles_subsection (xml, group_guid):
    group_files = xml.database.cursor()
    
    # 1 = select * from elgg_entity_subtypes where subtype='file';
    group_files.execute(qry.qry_group_posts, (group_guid, 1,))
    
    # 50 = select * from elgg_metastrings where string='file_enable';
    perm=qry.postcontent_permission(xml.database, group_guid, 50)
    
    xml.write_open_tag("arquivos",strf.permstr(perm))
    
    for (post_guid, post_title, post_desc, \
            owner_id, owner_name, owner_username, time)\
        in group_files:
        
        prefix='file/download/'
        file_link=strf.urlparticipa(prefix,str(post_guid))
        
        prefix='file/view/'
        post_attr=strf.pidstr(strf.urlparticipa(prefix,str(post_guid)))
        xml.write_open_tag("arquivo",post_attr)

        prefix='profile/'
        owner_attr=strf.uidstr(strf.urlparticipa(prefix,owner_username))
        xml.write_tag("autor",owner_name,owner_attr)
        xml.write_tag("titulo",post_title,'')
        xml.write_tag("data",strf.datestr(time),'')
        xml.write_tag("link",'',strf.hrefstr(file_link))
        xml.write_tag("descricao",strf.cdata(post_desc),'')
                    
        xml.write_comments(post_guid)
        
        xml.write_close_tag("arquivo")
        
    xml.write_close_tag("arquivos")
    
    group_files.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_groupforumtopics_subsection (xml, group_guid):
    group_forumtopics = xml.database.cursor()
    
    # 7 = select * from elgg_entity_subtypes where subtype='groupforumtopic';
    group_forumtopics.execute(qry.qry_group_posts, (group_guid, 7,))
    
    # 52 = select * from elgg_metastrings where string='forum_enable';
    perm=qry.postcontent_permission(xml.database, group_guid, 52)
    
    xml.write_open_tag("debates",strf.permstr(perm))
    
    for (post_guid, post_title, post_desc, \
        owner_id, owner_name, owner_username, time)\
        in group_forumtopics:
        
        prefix='discussion/view/'
        post_attr=strf.pidstr(strf.urlparticipa(prefix,str(post_guid)))
        xml.write_open_tag("debate",post_attr)

        prefix='profile/'
        owner_attr=strf.uidstr(strf.urlparticipa(prefix,owner_username))
        xml.write_tag("autor",owner_name,owner_attr)
        xml.write_tag("titulo",post_title,'')
        xml.write_tag("data",strf.datestr(time),'')
        xml.write_tag("texto",strf.cdata(post_desc),'')
            
        xml.write_comments(post_guid)
        
        xml.write_close_tag("debate")
        
    xml.write_close_tag("debates")
    
    group_forumtopics.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_groupbookmarks_subsection (xml, group_guid):
    group_bookmarks = xml.database.cursor()
    
    # 13 = select * from elgg_entity_subtypes where subtype='bookmarks';
    group_bookmarks.execute(qry.qry_group_posts, (group_guid, 13,))
    
    # 49 = select * from elgg_metastrings where string='bookmarks_enable';
    perm=qry.postcontent_permission(xml.database, group_guid, 49)
    
    xml.write_open_tag("favoritos",strf.permstr(perm))
    
    for (post_guid, post_title, post_desc, \
            owner_id, owner_name, owner_username, time)\
        in group_bookmarks:
            
        # 90 = select * from elgg_metastrings where string='address';
        bookmark_link=qry.post_content(xml.database, post_guid, 90)
        
        prefix='bookmarks/view/'
        post_attr=strf.pidstr(strf.urlparticipa(prefix,str(post_guid)))
        xml.write_open_tag("favorito",post_attr)

        prefix='profile/'
        owner_attr=strf.uidstr(strf.urlparticipa(prefix,owner_username))
        xml.write_tag("autor",owner_name,owner_attr)
        xml.write_tag("titulo",post_title,'')
        xml.write_tag("data",strf.datestr(time),'')
        xml.write_tag("link",'',strf.hrefstr(bookmark_link))
        xml.write_tag("descricao",strf.cdata(post_desc),'')
                            
        xml.write_comments(post_guid)
        
        xml.write_close_tag("favorito")
    
    xml.write_close_tag("favoritos")
    
    group_bookmarks.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_grouppages_subsection (xml, group_guid):
    group_pages = xml.database.cursor()
    
    # 14 = select * from elgg_entity_subtypes where subtype='page_top';
    group_pages.execute(qry.qry_group_posts, (group_guid, 14,))
    
    # 53 = select * from elgg_metastrings where string='pages_enable';
    perm=qry.postcontent_permission(xml.database, group_guid, 53)
    
    xml.write_open_tag("paginas",strf.permstr(perm))
    
    for (post_guid, post_title, post_desc,
            owner_id, owner_name, owner_username, time)\
        in group_pages:
        
        prefix='pages/view/'
        post_attr=strf.pidstr(strf.urlparticipa(prefix,str(post_guid)))
        xml.write_open_tag("pagina",post_attr)

        prefix='profile/'
        owner_attr=strf.uidstr(strf.urlparticipa(prefix,owner_username))
        xml.write_tag("autor",owner_name,owner_attr)
        xml.write_tag("titulo",post_title,'')
        xml.write_tag("data",strf.datestr(time),'')
        xml.write_tag("texto",strf.cdata(post_desc),'')
                    
        xml.write_comments(post_guid)
        
        xml.write_close_tag("pagina")
        
    xml.write_close_tag("paginas")
    
    group_pages.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_groupvideos_subsection (xml, group_guid):
    group_videos = xml.database.cursor()
    
    # 12 = select * from elgg_entity_subtypes where subtype='videos';
    group_videos.execute(qry.qry_group_posts, (group_guid, 12,))
    
    # 399 = select * from elgg_metastrings where string='videos_enable';
    perm=qry.postcontent_permission(xml.database, group_guid, 399)
    
    xml.write_open_tag("videos",strf.permstr(perm))
    
    for (post_guid, post_title, post_desc, \
            owner_id, owner_name, owner_username, time)\
        in group_videos:
            
        # 477 = select * from elgg_metastrings where string='video_url';
        video_link=qry.post_content(xml.database, post_guid, 477)
            
        prefix='videos/view/'
        post_attr=strf.pidstr(strf.urlparticipa(prefix,str(post_guid)))
        xml.write_open_tag("video",post_attr)

        prefix='profile/'
        owner_attr=strf.uidstr(strf.urlparticipa(prefix,owner_username))
        xml.write_tag("autor",owner_name,owner_attr)
        xml.write_tag("titulo",post_title,'')
        xml.write_tag("data",strf.datestr(time),'')
        xml.write_tag("link",'',strf.hrefstr(video_link))
        xml.write_tag("descricao",strf.cdata(post_desc),'')
            
        xml.write_comments(post_guid)
        
        xml.write_close_tag("video")
        
    xml.write_close_tag("videos")
    
    group_videos.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_groupevents_subsection (xml, group_guid):
    group_events = xml.database.cursor()
    
    # 6 = select * from elgg_entity_subtypes where subtype='calendar_event';
    group_events.execute(qry.qry_group_posts, (group_guid, 6,))
    
    # 54 = select * from elgg_metastrings where string='event_calendar_enable';
    perm=qry.postcontent_permission(xml.database, group_guid, 54)
    
    xml.write_open_tag("eventos",strf.permstr(perm))
    
    for (post_guid, post_title, post_desc, \
            owner_id, owner_name, owner_username, time)\
        in group_events:
            
        # 18 = select * from elgg_metastrings where string='venue';
        venue=qry.post_content(xml.database, post_guid, 18)
        
        # 20 = select * from elgg_metastrings where string='start_date';
        time_start=qry.post_content(xml.database, post_guid, 20)

        # 22 = select * from elgg_metastrings where string='end_date';
        time_end=qry.post_content(xml.database, post_guid, 22)
        
        # 26 = select * from elgg_metastrings where string='fees';
        fees=qry.post_content(xml.database, post_guid, 26)
        
        # 28 = select * from elgg_metastrings where string='contact';
        contact=qry.post_content(xml.database, post_guid, 28)
        
        # 30 = select * from elgg_metastrings where string='organizer';
        organizer=qry.post_content(xml.database, post_guid, 30)

        prefix='event_calendar/view/'
        post_attr=strf.pidstr(strf.urlparticipa(prefix,str(post_guid)))
        xml.write_open_tag("evento",post_attr)
        
        prefix='profile/'
        owner_attr=strf.uidstr(strf.urlparticipa(prefix,owner_username))
        xml.write_tag("autor",owner_name,owner_attr)
        xml.write_tag("titulo",post_title,'')
        xml.write_tag("data",strf.datestr(time),'')
        xml.write_tag("organizador",organizer,'')
        xml.write_tag("contato",contact,'')
        xml.write_tag("endereco",venue,'')
        xml.write_tag("data_inicio",strf.datestr(time_start),'')
        xml.write_tag("data_fim",strf.datestr(time_end),'')
        xml.write_tag("taxa_participacao",fees,'')
        xml.write_tag("descricao",strf.cdata(post_desc),'')
        
        xml.write_close_tag("evento")
        
        xml.write_comments(post_guid)
    
    xml.write_close_tag("eventos")
    
    group_events.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_groups_section(xml, \
    guid, title, desc, owner_id, owner_name, owner_username, time):

    # 45 = select * from elgg_metastrings where string='briefdescription';
    brief_desc=qry.post_content(xml.database, guid, 45)
    
    prefix='groups/profile/'
    group_attr=strf.cidstr(strf.urlparticipa(prefix,str(guid)))
    xml.write_open_tag("comunidade",group_attr)
    
    # Write all group's information
    prefix='profile/'
    owner_attr=strf.uidstr(strf.urlparticipa(prefix,owner_username))
    xml.write_tag("proprietario",owner_name,owner_attr)
    xml.write_tag("titulo",title,'')
    xml.write_tag("data",strf.datestr(time),'')
    xml.write_tag("descricao",strf.cdata(desc),'')
    xml.write_tag("breve_descricao",strf.cdata(brief_desc),'')
                                
    if qry.groupaccess_permission(xml.database, guid) == 'public':
            
        # Write a list of group member's name
        write_groupmembers_subsection(xml, guid)
        
        # Write a list, and all the info, of all posts made on the group.
        write_groupfiles_subsection(xml, guid)
        write_groupforumtopics_subsection(xml, guid)
        write_groupbookmarks_subsection(xml, guid)
        write_grouppages_subsection(xml, guid)
        write_groupvideos_subsection(xml, guid)
        write_groupevents_subsection(xml, guid)
        
    xml.write_close_tag("comunidade")
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_singlefile_groups_section (db, dir_results):
    
    groups_info = db.cursor()
    groups_info.execute(qry.qry_groups_info)

    xml_filename=dir_results+strf.date_today()+"_comunidades"+".xml"
    xml = OpendataXML(db,dir_results,xml_filename)
    
    xml.open_file()

    xml.write_open_tag("comunidades",'')
    
    for (guid, title, desc, owner_id, owner_name, owner_username, time)\
        in groups_info:
        
        write_groups_section(xml,\
            guid,title,desc,owner_id,owner_name,owner_username,time)
    
    xml.write_close_tag("comunidades")
    
    xml.close_file()
    
    groups_info.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_multifile_groups_section (db, dir_results):

    groups_info = db.cursor()
    groups_info.execute(qry.qry_groups_info)

    for (guid, title, desc, owner_id, owner_name, owner_username, time)\
        in groups_info:
            
        xml_filename=dir_results+'/groups/'+str(guid)+'.xml'
        xml = OpendataXML(db,dir_results,xml_filename)
        
        xml.open_file()
        
        write_groups_section(xml,\
            guid,title,desc,owner_id,owner_name,owner_username,time)
            
        xml.close_file()
        
    groups_info.close()
#--------------------------------------------------------------------#

######################################################################
