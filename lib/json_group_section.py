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

import queries_definition as qry
import json_support_functions as wrt

######################################################################
# Functions that write on JSON file

#-------------------------------------------------------------------#
def write_groupmembers_subsection (db, json, group_guid):
    group_members = db.cursor()
    group_members.execute(qry.qry_group_members, (group_guid,))
    
    qty=str(group_members.rowcount)
    wrt.write_tag(json,2,"quantidadeMembros",qty,",")
                
    wrt.write_open_tag(json,2,"membros","[")
    
    row=0
    for (user_id, user_name, user_username)\
        in group_members:
            
        row=row+1
            
        wrt.write_open_tag(json,3,"","{")
        
        prefix='profile/'
        user_attr=wrt.urlparticipa(prefix,user_username)
        
        wrt.write_open_tag(json,4,"usuario","{")
        wrt.write_tag(json,5,"uid",user_attr,",")
        wrt.write_tag(json,5,"nome",user_name,"")
        wrt.write_close_tag(json,4,"}",False)
        
        wrt.write_close_tag(json,3,"}",(row < group_members.rowcount))
        
    wrt.write_close_tag(json,2,"]",True)
    
    group_members.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_groupfiles_subsection (db, json, group_guid):
    group_files = db.cursor()
    
    # 1 = select * from elgg_entity_subtypes where subtype='file';
    group_files.execute(qry.qry_group_posts, (group_guid, 1,))
    
    # 50 = select * from elgg_metastrings where string='file_enable';
    perm=qry.postcontent_permission(db, group_guid, 50)
    
    wrt.write_tag(json,2,"arquivosHabilitado",perm,",")
    wrt.write_open_tag(json,2,"arquivos","[")
    
    row=0
    for (post_guid, post_title, post_desc, \
            owner_id, owner_name, owner_username, time)\
        in group_files:
            
        row=row+1
        
        wrt.write_open_tag(json,3,"","{")
        
        prefix='file/download/'
        file_link=wrt.urlparticipa(prefix,str(post_guid))
        
        prefix='file/view/'
        post_attr=wrt.urlparticipa(prefix,str(post_guid))
        wrt.write_tag(json,4,"pid",post_attr,",")

        prefix='profile/'
        owner_attr=wrt.urlparticipa(prefix,owner_username)
        
        wrt.write_open_tag(json,4,"autor","{")
        wrt.write_tag(json,5,"uid",owner_attr,",")
        wrt.write_tag(json,5,"nome",owner_name,"")
        wrt.write_close_tag(json,4,"}",True)
        
        wrt.write_tag(json,4,"titulo",post_title,",")
        wrt.write_tag(json,4,"data",wrt.datestr(time),",")
        wrt.write_tag(json,4,"link",file_link,",")
        wrt.write_tag(json,4,"descricao",post_desc,",")
                    
        wrt.write_comments(db,json,post_guid)
        
        wrt.write_close_tag(json,3,"}",(row < group_files.rowcount))
        
    wrt.write_close_tag(json,2,"]",True)
    
    group_files.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_groupforumtopics_subsection (db, json, group_guid):
    group_forumtopics = db.cursor()
    
    # 7 = select * from elgg_entity_subtypes where subtype='groupforumtopic';
    group_forumtopics.execute(qry.qry_group_posts, (group_guid, 7,))
    
    # 52 = select * from elgg_metastrings where string='forum_enable';
    perm=qry.postcontent_permission(db, group_guid, 52)
    
    wrt.write_tag(json,2,"debatesHabilitado",perm,",")
    wrt.write_open_tag(json,2,"debates","[")
    
    row=0
    for (post_guid, post_title, post_desc, \
        owner_id, owner_name, owner_username, time)\
        in group_forumtopics:
            
        row=row+1
        
        wrt.write_open_tag(json,3,"","{")
        
        prefix='discussion/view/'
        post_attr=wrt.urlparticipa(prefix,str(post_guid))
        wrt.write_tag(json,4,"pid",post_attr,",")

        prefix='profile/'
        owner_attr=wrt.urlparticipa(prefix,owner_username)
        
        wrt.write_open_tag(json,4,"autor","{")
        wrt.write_tag(json,5,"uid",owner_attr,",")
        wrt.write_tag(json,5,"nome",owner_name,"")
        wrt.write_close_tag(json,4,"}",True)
        
        wrt.write_tag(json,4,"titulo",post_title,",")
        wrt.write_tag(json,4,"data",wrt.datestr(time),",")
        wrt.write_tag(json,4,"texto",post_desc,",")
            
        wrt.write_comments(db,json,post_guid)
        
        wrt.write_close_tag(json,3,"}",(row < group_forumtopics.rowcount))
        
    wrt.write_close_tag(json,2,"]",True)
    
    group_forumtopics.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_groupbookmarks_subsection (db, json, group_guid):
    group_bookmarks = db.cursor()
    
    # 13 = select * from elgg_entity_subtypes where subtype='bookmarks';
    group_bookmarks.execute(qry.qry_group_posts, (group_guid, 13,))
    
    # 49 = select * from elgg_metastrings where string='bookmarks_enable';
    perm=qry.postcontent_permission(db, group_guid, 49)
    
    wrt.write_tag(json,2,"favoritosHabilitado",perm,",")
    wrt.write_open_tag(json,2,"favoritos","[")
    
    row=0
    for (post_guid, post_title, post_desc, \
            owner_id, owner_name, owner_username, time)\
        in group_bookmarks:
            
        row=row+1
        
        wrt.write_open_tag(json,3,"","{")
        
        # 90 = select * from elgg_metastrings where string='address';
        bookmark_link=qry.post_content(db,post_guid,90)
        
        prefix='bookmarks/view/'
        post_attr=wrt.urlparticipa(prefix,str(post_guid))
        wrt.write_tag(json,4,"pid",post_attr,",")

        prefix='profile/'
        owner_attr=wrt.urlparticipa(prefix,owner_username)
        
        wrt.write_open_tag(json,4,"autor","{")
        wrt.write_tag(json,5,"uid",owner_attr,",")
        wrt.write_tag(json,5,"nome",owner_name,"")
        wrt.write_close_tag(json,4,"}",True)
        
        wrt.write_tag(json,4,"titulo",post_title,",")
        wrt.write_tag(json,4,"data",wrt.datestr(time),",")
        wrt.write_tag(json,4,"link",bookmark_link,",")
        wrt.write_tag(json,4,"descricao",post_desc,",")
                            
        wrt.write_comments(db,json,post_guid)
        
        wrt.write_close_tag(json,3,"}",(row < group_bookmarks.rowcount))
    
    wrt.write_close_tag(json,2,"]",True)
    
    group_bookmarks.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_grouppages_subsection (db, json, group_guid):
    group_pages = db.cursor()
    
    # 14 = select * from elgg_entity_subtypes where subtype='page_top';
    group_pages.execute(qry.qry_group_posts, (group_guid, 14,))
    
    # 53 = select * from elgg_metastrings where string='pages_enable';
    perm=qry.postcontent_permission(db, group_guid, 53)
    
    wrt.write_tag(json,2,"paginasHabilitado",perm,",")
    wrt.write_open_tag(json,2,"paginas","[")
    
    row=0
    for (post_guid, post_title, post_desc,
            owner_id, owner_name, owner_username, time)\
        in group_pages:
            
        row=row+1
        
        wrt.write_open_tag(json,3,"","{")
        
        prefix='pages/view/'
        post_attr=wrt.urlparticipa(prefix,str(post_guid))
        wrt.write_tag(json,4,"pid",post_attr,",")

        prefix='profile/'
        owner_attr=wrt.urlparticipa(prefix,owner_username)
        
        wrt.write_open_tag(json,4,"autor","{")
        wrt.write_tag(json,5,"uid",owner_attr,",")
        wrt.write_tag(json,5,"nome",owner_name,"")
        wrt.write_close_tag(json,4,"}",True)
        
        wrt.write_tag(json,4,"titulo",post_title,",")
        wrt.write_tag(json,4,"data",wrt.datestr(time),",")
        wrt.write_tag(json,4,"texto",post_desc,",")
                    
        wrt.write_comments(db,json,post_guid)
        
        wrt.write_close_tag(json,3,"}",(row < group_pages.rowcount))
        
    wrt.write_close_tag(json,2,"]",True)
    
    group_pages.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_groupvideos_subsection (db, json, group_guid):
    group_videos = db.cursor()
    
    # 12 = select * from elgg_entity_subtypes where subtype='videos';
    group_videos.execute(qry.qry_group_posts, (group_guid, 12,))
    
    # 399 = select * from elgg_metastrings where string='videos_enable';
    perm=qry.postcontent_permission(db, group_guid, 399)
    
    wrt.write_tag(json,2,"videosHabilitado",perm,",")
    wrt.write_open_tag(json,2,"videos","[")
    
    row=0
    for (post_guid, post_title, post_desc, \
            owner_id, owner_name, owner_username, time)\
        in group_videos:
            
        row=row+1
            
        # 477 = select * from elgg_metastrings where string='video_url';
        video_link=qry.post_content(db,post_guid, 477)
        
        wrt.write_open_tag(json,3,"","{")
            
        prefix='videos/view/'
        post_attr=wrt.urlparticipa(prefix,str(post_guid))
        wrt.write_tag(json,4,"pid",post_attr,",")
        
        prefix='profile/'
        owner_attr=wrt.urlparticipa(prefix,owner_username)
        
        wrt.write_open_tag(json,4,"autor","{")
        wrt.write_tag(json,5,"uid",owner_attr,",")
        wrt.write_tag(json,5,"nome",owner_name,"")
        wrt.write_close_tag(json,4,"}",True)
        
        wrt.write_tag(json,4,"titulo",post_title,",")
        wrt.write_tag(json,4,"data",wrt.datestr(time),",")
        wrt.write_tag(json,4,"link",video_link,",")
        wrt.write_tag(json,4,"descricao",post_desc,",")
            
        wrt.write_comments(db,json,post_guid)

        wrt.write_close_tag(json,3,"}",(row < group_videos.rowcount))
        
    wrt.write_close_tag(json,2,"]",True)
    
    group_videos.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_groupevents_subsection (db, json, group_guid):
    group_events = db.cursor()
    
    # 6 = select * from elgg_entity_subtypes where subtype='calendar_event';
    group_events.execute(qry.qry_group_posts, (group_guid, 6,))
    
    # 54 = select * from elgg_metastrings where string='event_calendar_enable';
    perm=qry.postcontent_permission(db, group_guid, 54)
    
    wrt.write_tag(json,2,"eventosHabilitado",perm,",")
    wrt.write_open_tag(json,2,"eventos","[")
    
    row=0
    for (post_guid, post_title, post_desc, \
            owner_id, owner_name, owner_username, time)\
        in group_events:
            
        row=row+1
            
        wrt.write_open_tag(json,3,"","{")
            
        # 18 = select * from elgg_metastrings where string='venue';
        venue=qry.post_content(db, post_guid, 18)
        
        # 20 = select * from elgg_metastrings where string='start_date';
        time_start=qry.post_content(db, post_guid, 20)

        # 22 = select * from elgg_metastrings where string='end_date';
        time_end=qry.post_content(db, post_guid, 22)
        
        # 26 = select * from elgg_metastrings where string='fees';
        fees=qry.post_content(db, post_guid, 26)
        
        # 28 = select * from elgg_metastrings where string='contact';
        contact=qry.post_content(db, post_guid, 28)
        
        # 30 = select * from elgg_metastrings where string='organizer';
        organizer=qry.post_content(db, post_guid, 30)

        prefix='event_calendar/view/'
        post_attr=wrt.urlparticipa(prefix,str(post_guid))
        wrt.write_tag(json,4,"pid",post_attr,",")
                
        prefix='profile/'
        owner_attr=wrt.urlparticipa(prefix,owner_username)
        
        wrt.write_open_tag(json,4,"autor","{")
        wrt.write_tag(json,5,"uid",owner_attr,",")
        wrt.write_tag(json,5,"nome",owner_name,"")
        wrt.write_close_tag(json,4,"}",True)
        
        wrt.write_tag(json,4,"titulo",post_title,",")
        wrt.write_tag(json,4,"data",wrt.datestr(time),",")
        wrt.write_tag(json,4,"organizador",organizer,",")
        wrt.write_tag(json,4,"contato",contact,",")
        wrt.write_tag(json,4,"endereco",venue,",")
        wrt.write_tag(json,4,"dataInicio",wrt.datestr(time_start),",")
        wrt.write_tag(json,4,"dataFim",wrt.datestr(time_end),",")
        wrt.write_tag(json,4,"taxaParticipacao",fees,",")
        wrt.write_tag(json,4,"descricao",post_desc,",")
        
        wrt.write_comments(db,json,post_guid)
        
        wrt.write_close_tag(json,3,"}",(row < group_events.rowcount))
    
    wrt.write_close_tag(json,2,"]",False)
    
    group_events.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_groups_section (db, json,\
    guid, title, desc, owner_id, owner_name, owner_username, time):
    
    # 45 = select * from elgg_metastrings where string='briefdescription';
    brief_desc=qry.post_content(db,guid, 45)
        
    prefix='groups/profile/'
    group_attr=wrt.urlparticipa(prefix,str(guid))
    wrt.write_tag(json,2,"cid",group_attr,",")
    
    # Write all group's information
    prefix='profile/'
    owner_attr=wrt.urlparticipa(prefix,owner_username)
    
    wrt.write_open_tag(json,2,"proprietario","{")
    wrt.write_tag(json,3,"uid",owner_attr,",")
    wrt.write_tag(json,3,"nome",owner_name,"")
    wrt.write_close_tag(json,2,"}",True)
            
    wrt.write_tag(json,2,"titulo",title,",")
    wrt.write_tag(json,2,"data",wrt.datestr(time),",")
    wrt.write_tag(json,2,"descricao",desc,",")

    group_access = qry.groupaccess_permission(db, guid)
    
    if group_access == 'public':
        comma=","
    else:
        comma=""
        
    wrt.write_tag(json,2,"breveDescricao",brief_desc,comma)
                                        
    if group_access == 'public':
        
        # Write a list of group member's name
        write_groupmembers_subsection(db, json, guid)
    
        # Write a list, and all the info, of all posts made on the group.
        write_groupfiles_subsection(db, json, guid)
        write_groupforumtopics_subsection(db, json, guid)
        write_groupbookmarks_subsection(db, json, guid)
        write_grouppages_subsection(db, json, guid)
        write_groupvideos_subsection(db, json, guid)
        write_groupevents_subsection(db, json, guid)
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_singlefile_groups_section (db, dir_results):

    groups_info = db.cursor()
    groups_info.execute(qry.qry_groups_info)

    json_filename=dir_results+wrt.date_today()+"_comunidades"+".json"
    json = wrt.open_json_file(json_filename)
    
    wrt.write_open_tag(json,0,"","{")
    wrt.write_open_tag(json,0,"comunidades","[")
    
    row=0
    for (guid, title, desc, owner_id, owner_name, owner_username, time)\
        in groups_info:
            
        row=row+1
        
        wrt.write_open_tag(json,1,"","{")
            
        write_groups_section(db,json,\
            guid,title,desc,owner_id,owner_name,owner_username,time)
            
        wrt.write_close_tag(json,1,"}",(row < groups_info.rowcount))
        
    wrt.write_close_tag(json,0,"]",False)
    wrt.write_close_tag(json,0,"}",False)
    
    groups_info.close()
    
    json.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_multifile_groups_section (db, dir_results):

    groups_info = db.cursor()
    groups_info.execute(qry.qry_groups_info)

    for (guid, title, desc, owner_id, owner_name, owner_username, time)\
        in groups_info:
    
        json_filename=dir_results+'/groups/'+str(guid)+'.json'
        json = wrt.open_json_file(json_filename)
        
        wrt.write_open_tag(json,0,"","{")
        wrt.write_open_tag(json,1,"usuario","{")
            
        write_groups_section(db,json,\
            guid,title,desc,owner_id,owner_name,owner_username,time)
            
        wrt.write_close_tag(json,1,"}",False)
        wrt.write_close_tag(json,0,"}",False)
        
        json.close()
    
    groups_info.close()
#--------------------------------------------------------------------#

######################################################################
