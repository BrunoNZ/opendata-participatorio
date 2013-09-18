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

#--------------------------------------------------------------------#
def write_userfriends_subsection (xml, user_guid):
    friends_info = xml.database.cursor()
    friends_info.execute(qry.qry_user_friends, (user_guid))
    
    qty=str(friends_info.rowcount)
    xml.write_tag("quantidade_amigos",qty,'')
    
    xml.write_open_tag("amigos",'')
    for (friend_id, friend_name, friend_username) in friends_info:
        prefix='profile/'
        friend_attr=strf.uidstr(strf.urlparticipa(prefix,friend_username))
        xml.write_tag("usuario",friend_name,friend_attr)
    xml.write_close_tag("amigos")
        
    friends_info.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_userowngroup_subsection (xml, user_guid):        
    user_owngroups = xml.database.cursor()
    user_owngroups.execute(qry.qry_user_owngroups, (user_guid, user_guid, ))
        
    xml.write_open_tag("dono",'')
    for (group_id, group_title) in user_owngroups:
        prefix='groups/profile/'
        group_attr=strf.cidstr(strf.urlparticipa(prefix,str(group_id)))
        xml.write_tag("comunidade",group_title,group_attr)
    xml.write_close_tag("dono")
        
    user_owngroups.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_usermembergroup_subsection (xml, user_guid):
    user_membergroups = xml.database.cursor()
    user_membergroups.execute(qry.qry_user_membergroups, (user_guid, ))
        
    xml.write_open_tag("participante",'')
    for (group_id, group_title) in user_membergroups:
        prefix='groups/profile/'
        group_attr=strf.cidstr(strf.urlparticipa(prefix,str(group_id)))
        xml.write_tag("comunidade",group_title,group_attr)
    xml.write_close_tag("participante")
        
    user_membergroups.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_usergroups_subsection (xml, user_guid):
    xml.write_open_tag("comunidades",'')
    write_userowngroup_subsection(xml, user_guid)
    write_usermembergroup_subsection(xml, user_guid)
    xml.write_close_tag("comunidades")
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_userfiles_subsection (xml, user_guid):
    user_files = xml.database.cursor()
    
    # 1 = select * from elgg_entity_subtypes where subtype='file';
    user_files.execute(qry.qry_user_posts, (user_guid, user_guid, 1,))
    
    xml.write_open_tag("arquivos",'')
    
    for (post_guid, post_title, post_desc, time)\
        in user_files:
        
        prefix="file/download/"
        file_link=strf.urlparticipa(prefix,str(post_guid))
        
        prefix='file/view/'
        post_attr=strf.pidstr(strf.urlparticipa(prefix,str(post_guid)))
        xml.write_open_tag("arquivo",post_attr)
        
        xml.write_tag("titulo",post_title,'')
        xml.write_tag("data",strf.datestr(time),'')
        xml.write_tag("link",'',strf.hrefstr(file_link))
        xml.write_tag("descricao",strf.cdata(post_desc),'')
            
        xml.write_comments(post_guid)
        
        xml.write_close_tag("arquivo")
    
    xml.write_close_tag("arquivos")
    
    user_files.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_userblogs_subsection (xml, user_guid):
    user_blogs = xml.database.cursor()
    
    # 4 = select * from elgg_entity_subtypes where subtype='blog';
    user_blogs.execute(qry.qry_user_posts, (user_guid, user_guid, 4,))
    
    xml.write_open_tag("blogs",'')
    
    for (post_guid, post_title, post_desc, time)\
        in user_blogs:
                    
        post_excerpt = xml.database.cursor()
        
        # 64 = select * from elgg_metastrings where string='excerpt';
        post_excerpt=qry.post_content(xml.database, post_guid, 64)
            
        prefix='blog/view/'
        post_attr=strf.pidstr(strf.urlparticipa(prefix,str(post_guid)))
        xml.write_open_tag("blog",post_attr)

        xml.write_tag("titulo",post_title,'')
        xml.write_tag("data",strf.datestr(time),'')
        xml.write_tag("resumo",strf.cdata(post_excerpt),'')
        xml.write_tag("texto",strf.cdata(post_desc),'')
                    
        xml.write_comments(post_guid)
        
        xml.write_close_tag("blog")
            
    xml.write_close_tag("blogs")
    
    user_blogs.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_userbookmarks_subsection (xml, user_guid):
    user_bookmarks = xml.database.cursor()
    
    # 13 = select * from elgg_entity_subtypes where subtype='bookmarks';
    user_bookmarks.execute(qry.qry_user_posts, (user_guid, user_guid, 13,))
    
    xml.write_open_tag("favoritos",'')
    
    for (post_guid, post_title, post_desc, time)\
        in user_bookmarks:
                    
        # 90 = select * from elgg_metastrings where string='address';
        bookmark_link=qry.post_content(xml.database, post_guid, 90)
  
        prefix='bookmarks/view/'
        post_attr=strf.pidstr(strf.urlparticipa(prefix,str(post_guid)))
        xml.write_open_tag("favorito",post_attr)
    
        xml.write_tag("titulo",post_title,'')
        xml.write_tag("data",strf.datestr(time),'')
        xml.write_tag("link",'',strf.hrefstr(bookmark_link))
        xml.write_tag("descricao",strf.cdata(post_desc),'')
                    
        xml.write_comments(post_guid)
        
        xml.write_close_tag("favorito")
                
    xml.write_close_tag("favoritos")
    
    user_bookmarks.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#    
def write_userpages_subsection (xml, user_guid):
    user_pages = xml.database.cursor()
    
    # 14 = select * from elgg_entity_subtypes where subtype='page_top';
    user_pages.execute(qry.qry_user_posts, (user_guid, user_guid, 14,))
    
    xml.write_open_tag("paginas",'')
    
    for (post_guid, post_title, post_desc, time)\
        in user_pages:
        
        prefix='pages/view/'
        post_attr=strf.pidstr(strf.urlparticipa(prefix,str(post_guid)))
        xml.write_open_tag("pagina",post_attr)

        xml.write_tag("titulo",post_title,'')
        xml.write_tag("data",strf.datestr(time),'')
        xml.write_tag("texto",strf.cdata(post_desc),'')
                    
        xml.write_comments(post_guid)
        
        xml.write_close_tag("pagina")
        
    xml.write_close_tag("paginas")
    
    user_pages.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_uservideos_subsection (xml, user_guid):
    user_videos = xml.database.cursor()
    
    # 12 = select * from elgg_entity_subtypes where subtype='videos';
    user_videos.execute(qry.qry_user_posts, (user_guid, user_guid, 12,))
    
    xml.write_open_tag("videos",'')
    
    for (post_guid, post_title, post_desc, time)\
        in user_videos:
                    
        # 477 = select * from elgg_metastrings where string='video_url';
        video_link=qry.post_content(xml.database, post_guid, 477)
        
        prefix='videos/view/'
        post_attr=strf.pidstr(strf.urlparticipa(prefix,str(post_guid)))
        xml.write_open_tag("video",post_attr)
        
        xml.write_tag("titulo",post_title,'')
        xml.write_tag("data",strf.datestr(time),'')
        xml.write_tag("link",'',strf.hrefstr(video_link))
        xml.write_tag("descricao",strf.cdata(post_desc),'')
        
        xml.write_comments(post_guid)
        
        xml.write_close_tag("video")
        
    xml.write_close_tag("videos")
    
    user_videos.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_userevents_subsection (xml, user_guid):
    user_events = xml.database.cursor()
    
    # 6 = select * from elgg_entity_subtypes where subtype='calendar_event';
    user_events.execute(qry.qry_user_posts, (user_guid, user_guid, 6,))
    
    
    xml.write_open_tag("eventos",'')
    
    for (post_guid, post_title, post_desc, time)\
        in user_events:
            
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
        
        xml.write_tag("titulo",post_title,'')
        xml.write_tag("data",strf.datestr(time),'')
        xml.write_tag("organizador",organizer,'')
        xml.write_tag("contato",contact,'')
        xml.write_tag("endereco",venue,'')
        xml.write_tag("data_inicio",strf.datestr(time_start),'')
        xml.write_tag("data_fim",strf.datestr(time_end),'')
        xml.write_tag("taxa_participacao",fees,'')
        xml.write_tag("descricao",strf.cdata(post_desc),'')
        
        xml.write_comments(post_guid)
        
        xml.write_close_tag("evento")
    
    xml.write_close_tag("eventos")
    
    user_events.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#    
def write_users_section (xml, \
    guid, name, username):

    prefix='profile/'
    user_attr=strf.uidstr(strf.urlparticipa(prefix,username))
    xml.write_open_tag("usuario",user_attr)
    
    # Write all user's information
    xml.write_tag("nome",name,'')
        
    # Write a list of user friend's names
    write_userfriends_subsection(xml, guid)
    
    # Write a list of all groups that the user owns or belongs
    write_usergroups_subsection(xml, guid)
    
    # Write a list, and all the info, of all posts made by the user
    write_userfiles_subsection(xml, guid)
    write_userblogs_subsection(xml, guid)
    write_userbookmarks_subsection(xml, guid)
    write_userpages_subsection(xml, guid)
    write_uservideos_subsection(xml, guid)
    write_userevents_subsection(xml, guid)
    
    xml.write_close_tag("usuario")
#--------------------------------------------------------------------#    

#--------------------------------------------------------------------#    
def write_singlefile_users_section (db, dir_results):
   
    users_info = db.cursor()
    users_info.execute(qry.qry_users_info)
    
    xml_filename=dir_results+strf.date_today()+"_usuarios"+".xml"
    xml = OpendataXML(db,dir_results,xml_filename)

    xml.open_file()

    xml.write_open_tag("usuarios",'')
    
    for (guid, name, username)\
        in users_info:
            
        write_users_section(xml,\
            guid,name,username)        
    
    xml.write_close_tag("usuarios")
    
    xml.close_file()
    
    users_info.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#    
def write_multifile_users_section (db, dir_results):
   
    users_info = db.cursor()
    users_info.execute(qry.qry_users_info)
    
    for (guid, name, username)\
        in users_info:
        
        xml_filename=dir_results+'/users/'+str(guid)+'.xml'
        xml = OpendataXML(db,dir_results,xml_filename)
        
        xml.open_file()
    
        write_users_section(xml,\
            guid,name,username)        
        
        xml.close_file()
    
    users_info.close()
#--------------------------------------------------------------------#

######################################################################
