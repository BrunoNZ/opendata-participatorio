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

#--------------------------------------------------------------------#
def write_userfriends_subsection (json, user_guid):
    friends_info = json.database.cursor()
    friends_info.execute(qry.qry_user_friends, (user_guid))
    
    qty=str(friends_info.rowcount)
    json.write_tag("quantidadeAmigos",qty,",")
    
    json.write_open_tag("amigos","[")
    
    row=0
    for (friend_id, friend_name, friend_username)\
        in friends_info:
        
        row=row+1
            
        json.write_open_tag("","{")
        
        prefix='profile/'
        friend_attr=strf.urlparticipa(prefix,friend_username)
        
        json.write_tag("uid",friend_attr,",")
        json.write_tag("usuario",friend_name,"")
        
        json.write_close_tag("}",(row < friends_info.rowcount))
        
    json.write_close_tag("]",True)
        
    friends_info.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_userowngroup_subsection (json, user_guid):        
    user_owngroups = json.database.cursor()
    user_owngroups.execute(qry.qry_user_owngroups, (user_guid, user_guid, ))
        
    json.write_open_tag("dono","[")
    
    row=0
    for (group_id, group_title)\
        in user_owngroups:
            
        row=row+1
            
        json.write_open_tag("","{")
        
        prefix='groups/profile/'
        group_attr=strf.urlparticipa(prefix,str(group_id))
        
        json.write_tag("cid",group_attr,",")
        json.write_tag("titulo",group_title,"")
        
        json.write_close_tag("}",(row < user_owngroups.rowcount))
        
    json.write_close_tag("]",True)
        
    user_owngroups.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_usermembergroup_subsection (json, user_guid):
    user_membergroups = json.database.cursor()
    user_membergroups.execute(qry.qry_user_membergroups, (user_guid, ))
        
    json.write_open_tag("participante","[")
    
    row=0
    for (group_id, group_title)\
        in user_membergroups:
            
        row=row+1
            
        json.write_open_tag("","{")
        
        prefix='groups/profile/'
        group_attr=strf.urlparticipa(prefix,str(group_id))
        
        json.write_tag("cid",group_attr,",")
        json.write_tag("titulo",group_title,"")
        
        json.write_close_tag("}",(row < user_membergroups.rowcount))
        
    json.write_close_tag("]",False)
        
    user_membergroups.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_usergroups_subsection (json, user_guid):
    json.write_open_tag("comunidades","{")
    write_userowngroup_subsection(json, user_guid)
    write_usermembergroup_subsection(json, user_guid)
    json.write_close_tag("}",True)
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_userfiles_subsection (json, user_guid):
    user_files = json.database.cursor()
    
    # 1 = select * from elgg_entity_subtypes where subtype='file';
    user_files.execute(qry.qry_user_posts, (user_guid, user_guid, 1,))
    
    json.write_open_tag("arquivos","[")
    
    row=0
    for (post_guid, post_title, post_desc, time)\
        in user_files:
            
        row=row+1
        
        prefix="file/download/"
        file_link=strf.urlparticipa(prefix,str(post_guid))
        
        prefix='file/view/'
        post_attr=strf.urlparticipa(prefix,str(post_guid))
        
        json.write_open_tag("","{")
        
        json.write_tag("pid",post_attr,",")
        json.write_tag("titulo",post_title,",")
        json.write_tag("data",strf.datestr(time),",")
        json.write_tag("link",file_link,",")
        json.write_tag("descricao",post_desc,",")
            
        json.write_comments(post_guid)
        
        json.write_close_tag("}",(row < user_files.rowcount))
    
    json.write_close_tag("]",True)
    
    user_files.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_userblogs_subsection (json, user_guid):
    user_blogs = json.database.cursor()
    
    # 4 = select * from elgg_entity_subtypes where subtype='blog';
    user_blogs.execute(qry.qry_user_posts, (user_guid, user_guid, 4,))
    
    json.write_open_tag("blogs","[")
    
    row=0
    for (post_guid, post_title, post_desc, time)\
        in user_blogs:
            
        row=row+1
                    
        post_excerpt = json.database.cursor()
        
        # 64 = select * from elgg_metastrings where string='excerpt';
        post_excerpt=qry.post_content(json.database,post_guid,64)
            
        prefix='blog/view/'
        post_attr=strf.urlparticipa(prefix,str(post_guid))
        json.write_open_tag("","{")

        json.write_tag("pid",post_attr,",")
        json.write_tag("titulo",post_title,",")
        json.write_tag("data",strf.datestr(time),",")
        json.write_tag("resumo",post_excerpt,",")
        json.write_tag("texto",post_desc,",")
                    
        json.write_comments(post_guid)
        
        json.write_close_tag("}",(row < user_blogs.rowcount))
            
    json.write_close_tag("]",True)
    
    user_blogs.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_userbookmarks_subsection (json, user_guid):
    user_bookmarks = json.database.cursor()
    
    # 13 = select * from elgg_entity_subtypes where subtype='bookmarks';
    user_bookmarks.execute(qry.qry_user_posts, (user_guid, user_guid, 13,))
    
    json.write_open_tag("favoritos","[")
    
    row=0
    for (post_guid, post_title, post_desc, time)\
        in user_bookmarks:
            
        row=row+1
                    
        # 90 = select * from elgg_metastrings where string='address';
        bookmark_link=qry.post_content(json.database,post_guid,90)
  
        prefix='bookmarks/view/'
        post_attr=strf.urlparticipa(prefix,str(post_guid))
        json.write_open_tag("","{")
    
        json.write_tag("pid",post_attr,",")
        json.write_tag("titulo",post_title,",")
        json.write_tag("data",strf.datestr(time),",")
        json.write_tag("link",bookmark_link,",")
        json.write_tag("descricao",post_desc,",")
                    
        json.write_comments(post_guid)
        
        json.write_close_tag("}",(row < user_bookmarks.rowcount))
                
    json.write_close_tag("]",True)
    
    user_bookmarks.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#    
def write_userpages_subsection (json, user_guid):
    user_pages = json.database.cursor()
    
    # 14 = select * from elgg_entity_subtypes where subtype='page_top';
    user_pages.execute(qry.qry_user_posts, (user_guid, user_guid, 14,))
    
    json.write_open_tag("paginas","[")
    
    row=0
    for (post_guid, post_title, post_desc, time)\
        in user_pages:
        
        row=row+1
        
        prefix='pages/view/'
        post_attr=strf.urlparticipa(prefix,str(post_guid))
        
        json.write_open_tag("","{")

        json.write_tag("pid",post_attr,",")
        json.write_tag("titulo",post_title,",")
        json.write_tag("data",strf.datestr(time),",")
        json.write_tag("texto",post_desc,",")
                    
        json.write_comments(post_guid)
        
        json.write_close_tag("}",(row < user_pages.rowcount))
        
    json.write_close_tag("]",True)
    
    user_pages.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_uservideos_subsection (json, user_guid):
    user_videos = json.database.cursor()
    
    # 12 = select * from elgg_entity_subtypes where subtype='videos';
    user_videos.execute(qry.qry_user_posts, (user_guid, user_guid, 12,))
    
    json.write_open_tag("videos","[")
    
    row=0
    for (post_guid, post_title, post_desc, time)\
        in user_videos:
        
        row=row+1
                    
        # 477 = select * from elgg_metastrings where string='video_url';
        video_link=qry.post_content(json.database, post_guid, 477)
        
        prefix='videos/view/'
        post_attr=strf.urlparticipa(prefix,str(post_guid))
        
        json.write_open_tag("","{")
        
        json.write_tag("pid",post_attr,",")
        json.write_tag("titulo",post_title,",")
        json.write_tag("data",strf.datestr(time),",")
        json.write_tag("link",video_link,",")
        json.write_tag("descricao",post_desc,",")
        
        json.write_comments(post_guid)
        
        json.write_close_tag("}",(row < user_videos.rowcount))
        
    json.write_close_tag("]",True)
    
    user_videos.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_userevents_subsection (json, user_guid):
    user_events = json.database.cursor()
    
    # 6 = select * from elgg_entity_subtypes where subtype='calendar_event';
    user_events.execute(qry.qry_user_posts, (user_guid, user_guid, 6,))
    
    
    json.write_open_tag("eventos","[")
    
    row=0
    for (post_guid, post_title, post_desc, time)\
        in user_events:
            
        row=row+1
            
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
        
        json.write_open_tag("","{")
        
        json.write_tag("pid",post_attr,",")
        json.write_tag("titulo",post_title,",")
        json.write_tag("data",strf.datestr(time),",")
        json.write_tag("organizador",organizer,",")
        json.write_tag("contato",contact,",")
        json.write_tag("endereco",venue,",")
        json.write_tag("dataInicio",time_start,",")
        json.write_tag("dataFim",time_end,",")
        json.write_tag("taxaParticipacao",fees,",")
        json.write_tag("descricao",post_desc,",")
        
        json.write_comments(post_guid)
            
        json.write_close_tag("}",(row < user_events.rowcount))
    
    json.write_close_tag("]",False)
    
    user_events.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_users_section (json, \
    guid, name, username):

    prefix='profile/'
    user_attr=strf.urlparticipa(prefix,username)
    
    # Write all user's information
    json.write_tag("uid",user_attr,",")
    json.write_tag("nome",name,",")
    
    # Write a list of user friend's names
    write_userfriends_subsection(json, guid)
    
    # Write a list of all groups that the user owns or belongs
    write_usergroups_subsection(json, guid)
    
    # Write a list, and all the info, of all posts made by the user
    write_userfiles_subsection(json, guid)
    write_userblogs_subsection(json, guid)
    write_userbookmarks_subsection(json, guid)
    write_userpages_subsection(json, guid)
    write_uservideos_subsection(json, guid)
    write_userevents_subsection(json, guid)
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#    
def write_singlefile_users_section (db, dir_results):

    users_info = json.database.cursor()
    users_info.execute(qry.qry_users_info)
    
    json_filename=dir_results+strf.date_today()+"_usuarios"+".json"
    json = OpendataJSON(db,dir_results,json_filename)
    
    json.open_file()
    
    json.write_open_tag("","{")
    json.write_open_tag("usuarios","[")
    
    row=0
    for (guid, name, username)\
        in users_info:
            
        row=row+1
        
        json.write_open_tag("","{")
        
        write_users_section(json,\
            guid,name,username)
        
        json.write_close_tag("}",(row < users_info.rowcount))
    
    json.write_close_tag("]",False)
    json.write_close_tag("}",False)
    
    json.close_file()
    
    users_info.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#    
def write_multifile_users_section (db, dir_results):

    users_info = db.cursor()
    users_info.execute(qry.qry_users_info)
    
    for (guid, name, username)\
        in users_info:
            
        json_filename=dir_results+'/users/'+str(guid)+'.json'
        json = OpendataJSON(db,dir_results,json_filename)
        
        json.open_file()
            
        json.write_open_tag("","{")
        json.write_open_tag("usuario","{")
                
        write_users_section(json,\
            guid,name,username)
        
        json.write_close_tag("}",False)
        json.write_close_tag("}",False)
        
        json.close_file()
    
    users_info.close()
#--------------------------------------------------------------------#

######################################################################
