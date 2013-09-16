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
import write_support_functions as wrt

######################################################################
# Functions that write on JSON file

#--------------------------------------------------------------------#
def write_userfriends_subsection (db, json, user_guid):
    friends_info = db.cursor()
    friends_info.execute(qry.qry_user_friends, (user_guid))
    
    qty=str(friends_info.rowcount)
    wrt.write_tag(json,2,"quantidadeAmigos",qty,",")
    
    wrt.write_open_tag(json,2,"amigos","[")
    
    row=0
    for (friend_id, friend_name, friend_username)\
        in friends_info:
        
        row=row+1
            
        wrt.write_open_tag(json,3,"","{")
        
        prefix='profile/'
        friend_attr=wrt.urlparticipa(prefix,friend_username)
        
        wrt.write_tag(json,4,"uid",friend_attr,",")
        wrt.write_tag(json,4,"usuario",friend_name,"")
        
        wrt.write_close_tag(json,3,"}",(row < friends_info.rowcount))
        
    wrt.write_close_tag(json,2,"]",True)
        
    friends_info.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_userowngroup_subsection (db, json, user_guid):        
    user_owngroups = db.cursor()
    user_owngroups.execute(qry.qry_user_owngroups, (user_guid, user_guid, ))
        
    wrt.write_open_tag(json,3,"dono","[")
    
    row=0
    for (group_id, group_title)\
        in user_owngroups:
            
        row=row+1
            
        wrt.write_open_tag(json,4,"","{")
        
        prefix='groups/profile/'
        group_attr=wrt.urlparticipa(prefix,str(group_id))
        
        wrt.write_tag(json,5,"cid",group_attr,",")
        wrt.write_tag(json,5,"titulo",group_title,"")
        
        wrt.write_close_tag(json,4,"}",(row < user_owngroups.rowcount))
        
    wrt.write_close_tag(json,3,"]",True)
        
    user_owngroups.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_usermembergroup_subsection (db, json, user_guid):
    user_membergroups = db.cursor()
    user_membergroups.execute(qry.qry_user_membergroups, (user_guid, ))
        
    wrt.write_open_tag(json,3,"participante","[")
    
    row=0
    for (group_id, group_title)\
        in user_membergroups:
            
        row=row+1
            
        wrt.write_open_tag(json,4,"","{")
        
        prefix='groups/profile/'
        group_attr=wrt.urlparticipa(prefix,str(group_id))
        
        wrt.write_tag(json,5,"cid",group_attr,",")
        wrt.write_tag(json,5,"titulo",group_title,"")
        
        wrt.write_close_tag(json,4,"}",(row < user_membergroups.rowcount))
        
    wrt.write_close_tag(json,3,"]",False)
        
    user_membergroups.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_usergroups_subsection (db, json, user_guid):
    wrt.write_open_tag(json,2,"comunidades","{")
    write_userowngroup_subsection(db, json, user_guid)
    write_usermembergroup_subsection(db, json, user_guid)
    wrt.write_close_tag(json,2,"}",True)
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_userfiles_subsection (db, json, user_guid):
    user_files = db.cursor()
    
    # 1 = select * from elgg_entity_subtypes where subtype='file';
    user_files.execute(qry.qry_user_posts, (user_guid, user_guid, 1,))
    
    wrt.write_open_tag(json,2,"arquivos","[")
    
    row=0
    for (post_guid, post_title, post_desc, time)\
        in user_files:
            
        row=row+1
        
        prefix="file/download/"
        file_link=wrt.urlparticipa(prefix,str(post_guid))
        
        prefix='file/view/'
        post_attr=wrt.urlparticipa(prefix,str(post_guid))
        
        wrt.write_open_tag(json,3,"","{")
        
        wrt.write_tag(json,4,"pid",post_attr,",")
        wrt.write_tag(json,4,"titulo",post_title,",")
        wrt.write_tag(json,4,"data",wrt.datestr(time),",")
        wrt.write_tag(json,4,"link",file_link,",")
        wrt.write_tag(json,4,"descricao",post_desc,",")
            
        wrt.write_comments(db,json,post_guid)
        
        wrt.write_close_tag(json,3,"}",(row < user_files.rowcount))
    
    wrt.write_close_tag(json,2,"]",True)
    
    user_files.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_userblogs_subsection (db, json, user_guid):
    user_blogs = db.cursor()
    
    # 4 = select * from elgg_entity_subtypes where subtype='blog';
    user_blogs.execute(qry.qry_user_posts, (user_guid, user_guid, 4,))
    
    wrt.write_open_tag(json,2,"blogs","[")
    
    row=0
    for (post_guid, post_title, post_desc, time)\
        in user_blogs:
            
        row=row+1
                    
        post_excerpt = db.cursor()
        
        # 64 = select * from elgg_metastrings where string='excerpt';
        post_excerpt=wrt.post_content(db,post_guid,64)
            
        prefix='blog/view/'
        post_attr=wrt.urlparticipa(prefix,str(post_guid))
        wrt.write_open_tag(json,3,"","{")

        wrt.write_tag(json,4,"pid",post_attr,",")
        wrt.write_tag(json,4,"titulo",post_title,",")
        wrt.write_tag(json,4,"data",wrt.datestr(time),",")
        wrt.write_tag(json,4,"resumo",post_excerpt,",")
        wrt.write_tag(json,4,"texto",post_desc,",")
                    
        wrt.write_comments(db,json,post_guid)
        
        wrt.write_close_tag(json,3,"}",(row < user_blogs.rowcount))
            
    wrt.write_close_tag(json,2,"]",True)
    
    user_blogs.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_userbookmarks_subsection (db, json, user_guid):
    user_bookmarks = db.cursor()
    
    # 13 = select * from elgg_entity_subtypes where subtype='bookmarks';
    user_bookmarks.execute(qry.qry_user_posts, (user_guid, user_guid, 13,))
    
    wrt.write_open_tag(json,2,"favoritos","[")
    
    row=0
    for (post_guid, post_title, post_desc, time)\
        in user_bookmarks:
            
        row=row+1
                    
        # 90 = select * from elgg_metastrings where string='address';
        bookmark_link=wrt.post_content(db,post_guid,90)
  
        prefix='bookmarks/view/'
        post_attr=wrt.urlparticipa(prefix,str(post_guid))
        wrt.write_open_tag(json,3,"","{")
    
        wrt.write_tag(json,4,"pid",post_attr,",")
        wrt.write_tag(json,4,"titulo",post_title,",")
        wrt.write_tag(json,4,"data",wrt.datestr(time),",")
        wrt.write_tag(json,4,"link",bookmark_link,",")
        wrt.write_tag(json,4,"descricao",post_desc,",")
                    
        wrt.write_comments(db,json,post_guid)
        
        wrt.write_close_tag(json,3,"}",(row < user_bookmarks.rowcount))
                
    wrt.write_close_tag(json,2,"]",True)
    
    user_bookmarks.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#    
def write_userpages_subsection (db, json, user_guid):
    user_pages = db.cursor()
    
    # 14 = select * from elgg_entity_subtypes where subtype='page_top';
    user_pages.execute(qry.qry_user_posts, (user_guid, user_guid, 14,))
    
    wrt.write_open_tag(json,2,"paginas","[")
    
    row=0
    for (post_guid, post_title, post_desc, time)\
        in user_pages:
        
        row=row+1
        
        prefix='pages/view/'
        post_attr=wrt.urlparticipa(prefix,str(post_guid))
        
        wrt.write_open_tag(json,3,"","{")

        wrt.write_tag(json,4,"pid",post_attr,",")
        wrt.write_tag(json,4,"titulo",post_title,",")
        wrt.write_tag(json,4,"data",wrt.datestr(time),",")
        wrt.write_tag(json,4,"texto",post_desc,",")
                    
        wrt.write_comments(db,json,post_guid)
        
        wrt.write_close_tag(json,3,"}",(row < user_pages.rowcount))
        
    wrt.write_close_tag(json,2,"]",True)
    
    user_pages.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_uservideos_subsection (db, json, user_guid):
    user_videos = db.cursor()
    
    # 12 = select * from elgg_entity_subtypes where subtype='videos';
    user_videos.execute(qry.qry_user_posts, (user_guid, user_guid, 12,))
    
    wrt.write_open_tag(json,2,"videos","[")
    
    row=0
    for (post_guid, post_title, post_desc, time)\
        in user_videos:
        
        row=row+1
                    
        # 477 = select * from elgg_metastrings where string='video_url';
        video_link=wrt.post_content(db, post_guid, 477)
        
        prefix='videos/view/'
        post_attr=wrt.urlparticipa(prefix,str(post_guid))
        
        wrt.write_open_tag(json,3,"","{")
        
        wrt.write_tag(json,4,"pid",post_attr,",")
        wrt.write_tag(json,4,"titulo",post_title,",")
        wrt.write_tag(json,4,"data",wrt.datestr(time),",")
        wrt.write_tag(json,4,"link",video_link,",")
        wrt.write_tag(json,4,"descricao",post_desc,",")
        
        wrt.write_comments(db,json,post_guid)
        
        wrt.write_close_tag(json,3,"}",(row < user_videos.rowcount))
        
    wrt.write_close_tag(json,2,"]",True)
    
    user_videos.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_userevents_subsection (db, json, user_guid):
    user_events = db.cursor()
    
    # 6 = select * from elgg_entity_subtypes where subtype='calendar_event';
    user_events.execute(qry.qry_user_posts, (user_guid, user_guid, 6,))
    
    
    wrt.write_open_tag(json,2,"eventos","[")
    
    row=0
    for (post_guid, post_title, post_desc, time)\
        in user_events:
            
        row=row+1
            
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
        post_attr=wrt.urlparticipa(prefix,str(post_guid))
        
        wrt.write_open_tag(json,3,"","{")
        
        wrt.write_tag(json,4,"pid",post_attr,",")
        wrt.write_tag(json,4,"titulo",post_title,",")
        wrt.write_tag(json,4,"data",wrt.datestr(time),",")
        wrt.write_tag(json,4,"organizador",organizer,",")
        wrt.write_tag(json,4,"contato",contact,",")
        wrt.write_tag(json,4,"endereco",venue,",")
        wrt.write_tag(json,4,"dataInicio",time_start,",")
        wrt.write_tag(json,4,"dataFim",time_end,",")
        wrt.write_tag(json,4,"taxaParticipacao",fees,",")
        wrt.write_tag(json,4,"descricao",post_desc,",")
        
        wrt.write_comments(db,json,post_guid)
            
        wrt.write_close_tag(json,3,"}",(row < user_events.rowcount))
    
    wrt.write_close_tag(json,2,"]",False)
    
    user_events.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#    
def write_users_section (db, json_filename):
    
    json = wrt.open_json_file(json_filename)
    
    wrt.write_open_tag(json,0,"","{")
    wrt.write_open_tag(json,0,"usuarios","[")
    
    users_info = db.cursor()
    users_info.execute(qry.qry_users_info)
    
    row=0
    for (guid, name, username)\
        in users_info:
            
        row=row+1
        
        prefix='profile/'
        user_attr=wrt.urlparticipa(prefix,username)
        
        wrt.write_open_tag(json,1,"","{")
        
        # Write all user's information
        wrt.write_tag(json,2,"uid",user_attr,",")
        wrt.write_tag(json,2,"nome",name,",")
            
        # Write a list of user friend's names
        write_userfriends_subsection(db, json, guid)
        
        # Write a list of all groups that the user owns or belongs
        write_usergroups_subsection(db, json, guid)
        
        # Write a list, and all the info, of all posts made by the user
        write_userfiles_subsection(db, json, guid)
        write_userblogs_subsection(db, json, guid)
        write_userbookmarks_subsection(db, json, guid)
        write_userpages_subsection(db, json, guid)
        write_uservideos_subsection(db, json, guid)
        write_userevents_subsection(db, json, guid)
        
        wrt.write_close_tag(json,1,"}",(row < users_info.rowcount))
    
    wrt.write_close_tag(json,0,"]",False)
    wrt.write_close_tag(json,0,"}",False)
    
    users_info.close()
    
    json.close()
#--------------------------------------------------------------------#

######################################################################
