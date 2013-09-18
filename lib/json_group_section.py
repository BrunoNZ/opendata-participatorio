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

from opendata_json_class import OpendataJSON

import opendata_queries_definition as qry
import opendata_string_functions as strf

######################################################################
# Functions that write on JSON file

#-------------------------------------------------------------------#
def write_groupmembers_subsection (json, group_guid):
    group_members = json.database.cursor()
    group_members.execute(qry.qry_group_members, (group_guid,))
    
    qty=str(group_members.rowcount)
    json.write_tag("quantidadeMembros",qty,",")
                
    json.write_open_tag("membros","[")
    
    row=0
    for (user_id, user_name, user_username)\
        in group_members:
            
        row=row+1
            
        json.write_open_tag("","{")
        
        prefix='profile/'
        user_attr=strf.urlparticipa(prefix,user_username)
        
        json.write_open_tag("usuario","{")
        json.write_tag("uid",user_attr,",")
        json.write_tag("nome",user_name,"")
        json.write_close_tag("}",False)
        
        json.write_close_tag("}",(row < group_members.rowcount))
        
    json.write_close_tag("]",True)
    
    group_members.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_groupfiles_subsection (json, group_guid):
    group_files = json.database.cursor()
    
    # 1 = select * from elgg_entity_subtypes where subtype='file';
    group_files.execute(qry.qry_group_posts, (group_guid, 1,))
    
    # 50 = select * from elgg_metastrings where string='file_enable';
    perm=qry.postcontent_permission(json.database, group_guid, 50)
    
    json.write_tag("arquivosHabilitado",perm,",")
    json.write_open_tag("arquivos","[")
    
    row=0
    for (post_guid, post_title, post_desc, \
            owner_id, owner_name, owner_username, time)\
        in group_files:
            
        row=row+1
        
        json.write_open_tag("","{")
        
        prefix='file/download/'
        file_link=strf.urlparticipa(prefix,str(post_guid))
        
        prefix='file/view/'
        post_attr=strf.urlparticipa(prefix,str(post_guid))
        json.write_tag("pid",post_attr,",")

        prefix='profile/'
        owner_attr=strf.urlparticipa(prefix,owner_username)
        
        json.write_open_tag("autor","{")
        json.write_tag("uid",owner_attr,",")
        json.write_tag("nome",owner_name,"")
        json.write_close_tag("}",True)
        
        json.write_tag("titulo",post_title,",")
        json.write_tag("data",strf.datestr(time),",")
        json.write_tag("link",file_link,",")
        json.write_tag("descricao",post_desc,",")
                    
        json.write_comments(post_guid)
        
        json.write_close_tag("}",(row < group_files.rowcount))
        
    json.write_close_tag("]",True)
    
    group_files.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_groupforumtopics_subsection (json, group_guid):
    group_forumtopics = json.database.cursor()
    
    # 7 = select * from elgg_entity_subtypes where subtype='groupforumtopic';
    group_forumtopics.execute(qry.qry_group_posts, (group_guid, 7,))
    
    # 52 = select * from elgg_metastrings where string='forum_enable';
    perm=qry.postcontent_permission(json.database, group_guid, 52)
    
    json.write_tag("debatesHabilitado",perm,",")
    json.write_open_tag("debates","[")
    
    row=0
    for (post_guid, post_title, post_desc, \
        owner_id, owner_name, owner_username, time)\
        in group_forumtopics:
            
        row=row+1
        
        json.write_open_tag("","{")
        
        prefix='discussion/view/'
        post_attr=strf.urlparticipa(prefix,str(post_guid))
        json.write_tag("pid",post_attr,",")

        prefix='profile/'
        owner_attr=strf.urlparticipa(prefix,owner_username)
        
        json.write_open_tag("autor","{")
        json.write_tag("uid",owner_attr,",")
        json.write_tag("nome",owner_name,"")
        json.write_close_tag("}",True)
        
        json.write_tag("titulo",post_title,",")
        json.write_tag("data",strf.datestr(time),",")
        json.write_tag("texto",post_desc,",")
            
        json.write_comments(post_guid)
        
        json.write_close_tag("}",(row < group_forumtopics.rowcount))
        
    json.write_close_tag("]",True)
    
    group_forumtopics.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_groupbookmarks_subsection (json, group_guid):
    group_bookmarks = json.database.cursor()
    
    # 13 = select * from elgg_entity_subtypes where subtype='bookmarks';
    group_bookmarks.execute(qry.qry_group_posts, (group_guid, 13,))
    
    # 49 = select * from elgg_metastrings where string='bookmarks_enable';
    perm=qry.postcontent_permission(json.database, group_guid, 49)
    
    json.write_tag("favoritosHabilitado",perm,",")
    json.write_open_tag("favoritos","[")
    
    row=0
    for (post_guid, post_title, post_desc, \
            owner_id, owner_name, owner_username, time)\
        in group_bookmarks:
            
        row=row+1
        
        json.write_open_tag("","{")
        
        # 90 = select * from elgg_metastrings where string='address';
        bookmark_link=qry.post_content(json.database, post_guid, 90)
        
        prefix='bookmarks/view/'
        post_attr=strf.urlparticipa(prefix,str(post_guid))
        json.write_tag("pid",post_attr,",")

        prefix='profile/'
        owner_attr=strf.urlparticipa(prefix,owner_username)
        
        json.write_open_tag("autor","{")
        json.write_tag("uid",owner_attr,",")
        json.write_tag("nome",owner_name,"")
        json.write_close_tag("}",True)
        
        json.write_tag("titulo",post_title,",")
        json.write_tag("data",strf.datestr(time),",")
        json.write_tag("link",bookmark_link,",")
        json.write_tag("descricao",post_desc,",")
                            
        json.write_comments(post_guid)
        
        json.write_close_tag("}",(row < group_bookmarks.rowcount))
    
    json.write_close_tag("]",True)
    
    group_bookmarks.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_grouppages_subsection (json, group_guid):
    group_pages = json.database.cursor()
    
    # 14 = select * from elgg_entity_subtypes where subtype='page_top';
    group_pages.execute(qry.qry_group_posts, (group_guid, 14,))
    
    # 53 = select * from elgg_metastrings where string='pages_enable';
    perm=qry.postcontent_permission(json.database, group_guid, 53)
    
    json.write_tag("paginasHabilitado",perm,",")
    json.write_open_tag("paginas","[")
    
    row=0
    for (post_guid, post_title, post_desc,
            owner_id, owner_name, owner_username, time)\
        in group_pages:
            
        row=row+1
        
        json.write_open_tag("","{")
        
        prefix='pages/view/'
        post_attr=strf.urlparticipa(prefix,str(post_guid))
        json.write_tag("pid",post_attr,",")

        prefix='profile/'
        owner_attr=strf.urlparticipa(prefix,owner_username)
        
        json.write_open_tag("autor","{")
        json.write_tag("uid",owner_attr,",")
        json.write_tag("nome",owner_name,"")
        json.write_close_tag("}",True)
        
        json.write_tag("titulo",post_title,",")
        json.write_tag("data",strf.datestr(time),",")
        json.write_tag("texto",post_desc,",")
                    
        json.write_comments(post_guid)
        
        json.write_close_tag("}",(row < group_pages.rowcount))
        
    json.write_close_tag("]",True)
    
    group_pages.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_groupvideos_subsection (json, group_guid):
    group_videos = json.database.cursor()
    
    # 12 = select * from elgg_entity_subtypes where subtype='videos';
    group_videos.execute(qry.qry_group_posts, (group_guid, 12,))
    
    # 399 = select * from elgg_metastrings where string='videos_enable';
    perm=qry.postcontent_permission(json.database, group_guid, 399)
    
    json.write_tag("videosHabilitado",perm,",")
    json.write_open_tag("videos","[")
    
    row=0
    for (post_guid, post_title, post_desc, \
            owner_id, owner_name, owner_username, time)\
        in group_videos:
            
        row=row+1
            
        # 477 = select * from elgg_metastrings where string='video_url';
        video_link=qry.post_content(json.database, post_guid, 477)
        
        json.write_open_tag("","{")
            
        prefix='videos/view/'
        post_attr=strf.urlparticipa(prefix,str(post_guid))
        json.write_tag("pid",post_attr,",")
        
        prefix='profile/'
        owner_attr=strf.urlparticipa(prefix,owner_username)
        
        json.write_open_tag("autor","{")
        json.write_tag("uid",owner_attr,",")
        json.write_tag("nome",owner_name,"")
        json.write_close_tag("}",True)
        
        json.write_tag("titulo",post_title,",")
        json.write_tag("data",strf.datestr(time),",")
        json.write_tag("link",video_link,",")
        json.write_tag("descricao",post_desc,",")
            
        json.write_comments(post_guid)

        json.write_close_tag("}",(row < group_videos.rowcount))
        
    json.write_close_tag("]",True)
    
    group_videos.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_groupevents_subsection (json, group_guid):
    group_events = json.database.cursor()
    
    # 6 = select * from elgg_entity_subtypes where subtype='calendar_event';
    group_events.execute(qry.qry_group_posts, (group_guid, 6,))
    
    # 54 = select * from elgg_metastrings where string='event_calendar_enable';
    perm=qry.postcontent_permission(json.database, group_guid, 54)
    
    json.write_tag("eventosHabilitado",perm,",")
    json.write_open_tag("eventos","[")
    
    row=0
    for (post_guid, post_title, post_desc, \
            owner_id, owner_name, owner_username, time)\
        in group_events:
            
        row=row+1
            
        json.write_open_tag("","{")
            
        # 18 = select * from elgg_metastrings where string='venue';
        venue=qry.post_content(json.database, post_guid, 18)
        
        # 20 = select * from elgg_metastrings where string='start_date';
        time_start=qry.post_content(json.database, post_guid, 20)

        # 22 = select * from elgg_metastrings where string='end_date';
        time_end=qry.post_content(json.database, post_guid, 22)
        
        # 26 = select * from elgg_metastrings where string='fees';
        fees=qry.post_content(json.database, post_guid, 26)
        
        # 28 = select * from elgg_metastrings where string='contact';
        contact=qry.post_content(json.database, post_guid, 28)
        
        # 30 = select * from elgg_metastrings where string='organizer';
        organizer=qry.post_content(json.database, post_guid, 30)

        prefix='event_calendar/view/'
        post_attr=strf.urlparticipa(prefix,str(post_guid))
        json.write_tag("pid",post_attr,",")
                
        prefix='profile/'
        owner_attr=strf.urlparticipa(prefix,owner_username)
        
        json.write_open_tag("autor","{")
        json.write_tag("uid",owner_attr,",")
        json.write_tag("nome",owner_name,"")
        json.write_close_tag("}",True)
        
        json.write_tag("titulo",post_title,",")
        json.write_tag("data",strf.datestr(time),",")
        json.write_tag("organizador",organizer,",")
        json.write_tag("contato",contact,",")
        json.write_tag("endereco",venue,",")
        json.write_tag("dataInicio",strf.datestr(time_start),",")
        json.write_tag("dataFim",strf.datestr(time_end),",")
        json.write_tag("taxaParticipacao",fees,",")
        json.write_tag("descricao",post_desc,",")
        
        json.write_comments(post_guid)
        
        json.write_close_tag("}",(row < group_events.rowcount))
    
    json.write_close_tag("]",False)
    
    group_events.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_groups_section (json,\
    guid, title, desc, owner_id, owner_name, owner_username, time):
    
    # 45 = select * from elgg_metastrings where string='briefdescription';
    brief_desc=qry.post_content(json.database, guid, 45)
        
    prefix='groups/profile/'
    group_attr=strf.urlparticipa(prefix,str(guid))
    json.write_tag("cid",group_attr,",")
    
    # Write all group's information
    prefix='profile/'
    owner_attr=strf.urlparticipa(prefix,owner_username)
    
    json.write_open_tag("proprietario","{")
    json.write_tag("uid",owner_attr,",")
    json.write_tag("nome",owner_name,"")
    json.write_close_tag("}",True)
            
    json.write_tag("titulo",title,",")
    json.write_tag("data",strf.datestr(time),",")
    json.write_tag("descricao",desc,",")

    group_access = qry.groupaccess_permission(json.database, guid)
    
    if group_access == 'public':
        comma=","
    else:
        comma=""
        
    json.write_tag("breveDescricao",brief_desc,comma)
                                        
    if group_access == 'public':
        
        # Write a list of group member's name
        write_groupmembers_subsection(json, guid)
    
        # Write a list, and all the info, of all posts made on the group.
        write_groupfiles_subsection(json, guid)
        write_groupforumtopics_subsection(json, guid)
        write_groupbookmarks_subsection(json, guid)
        write_grouppages_subsection(json, guid)
        write_groupvideos_subsection(json, guid)
        write_groupevents_subsection(json, guid)
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_singlefile_groups_section (db, dir_results):

    groups_info = json.database.cursor()
    groups_info.execute(qry.qry_groups_info)

    json_filename=dir_results+strf.date_today()+"_comunidades"+".json"
    json = OpendataJSON(db,dir_results,json_filename)
    
    json.open_file()
    
    json.write_open_tag("","{")
    json.write_open_tag("comunidades","[")
    
    row=0
    for (guid, title, desc, owner_id, owner_name, owner_username, time)\
        in groups_info:
            
        row=row+1
        
        json.write_open_tag("","{")
            
        write_groups_section(json,\
            guid,title,desc,owner_id,owner_name,owner_username,time)
            
        json.write_close_tag("}",(row < groups_info.rowcount))
        
    json.write_close_tag("]",False)
    json.write_close_tag("}",False)
    
    json.close_file()
    
    groups_info.close()
#--------------------------------------------------------------------#

#-----------------------------------------------------------------w---#
def write_multifile_groups_section (db, dir_results):

    groups_info = db.cursor()
    groups_info.execute(qry.qry_groups_info)

    for (guid, title, desc, owner_id, owner_name, owner_username, time)\
        in groups_info:
    
        json_filename=dir_results+'/groups/'+str(guid)+'.json'
        json = OpendataJSON(db,dir_results,json_filename)
        
        json.open_file()
        
        json.write_open_tag("","{")
        json.write_open_tag("usuario","{")
            
        write_groups_section(json,\
            guid,title,desc,owner_id,owner_name,owner_username,time)
            
        json.write_close_tag("}",False)
        json.write_close_tag("}",False)
        
        json.close_file()
    
    groups_info.close()
#--------------------------------------------------------------------#

######################################################################
