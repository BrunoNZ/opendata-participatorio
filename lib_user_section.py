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

#--------------------------------------------------------------------#
# Definition of XML Levels initial space
# These variables are meant to be used in front of every
# string written on the xml file to make the correct indentation
l1="\t"
l2="\t\t"
l3="\t\t\t"
l4="\t\t\t\t"
l5="\t\t\t\t\t"
l6="\t\t\t\t\t\t"
l7="\t\t\t\t\t\t\t"
#--------------------------------------------------------------------#

######################################################################
# Query definitions:

#--------------------------------------------------------------------#
# Argument: None
# Return: All member instances, and its info, from database.
qry_users_info = \
("	SELECT u.guid, u.name, u.username \
	FROM elgg_entities e, elgg_users_entity u \
	WHERE e.guid = u.guid \
    AND (e.access_id = 1 OR e.access_id = 2); ")
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
# Argument: Group_ID / InfoType_ID
# Return: All InfoTypes' posts made by this group.
qry_user_posts = \
("	SELECT o.guid, o.title, o.description, e.time_created \
	FROM elgg_entities e, elgg_objects_entity o \
	WHERE e.guid = o.guid \
    AND (e.access_id = 1 OR e.access_id = 2) \
    AND e.owner_guid = %s AND e.container_guid = %s AND e.subtype = %s \
    ORDER BY e.time_created ASC; ")
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
# Argument: Post_ID
# Return: All comments, and its info, made on the post.
qry_post_comments = \
("	SELECT u.guid, u.name, u.username, m.string, a.time_created \
	FROM elgg_annotations a, elgg_metastrings m, elgg_users_entity u \
	WHERE a.value_id = m.id AND a.owner_guid = u.guid \
    AND (a.access_id = 1 OR a.access_id = 2) \
    AND a.entity_guid = %s \
    ORDER BY a.time_created ASC; ")
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
# Argument: User_ID
# Return: All user friends' name
qry_user_friends = \
("	SELECT u.guid, u.name, u.username \
	FROM elgg_users_entity u, elgg_entity_relationships r \
	WHERE u.guid = r.guid_two \
	AND r.guid_one = %s AND r.relationship = 'friend'; ")
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
# Argument: User_ID
# Return: Name of all the groups owned/created by the user.
qry_user_owngroups = \
("	SELECT g.guid, g.name \
	FROM elgg_entities e, elgg_groups_entity g \
	WHERE e.guid = g.guid \
	AND e.owner_guid = %s AND e.container_guid = %s; ")
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
# Argument: User_ID
# Return: Name of all the groups that the user is a member.
qry_user_membergroups = \
("	SELECT g.guid, g.name \
	FROM elgg_entity_relationships r, elgg_groups_entity g \
	WHERE r.guid_two = g.guid \
	AND r.relationship = 'member' AND r.guid_one = %s; ")
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
# Argument: Post_ID / InfoType_ID
# Return: Essential information about the group or post, such as
#   blog's excerpts and bookmark's link
qry_post_content = \
("  SELECT s.string\
    FROM elgg_metadata d, elgg_metastrings s \
    WHERE d.value_id = s.id \
    AND d.entity_guid = %s AND d.name_id = %s; ")
#--------------------------------------------------------------------#

######################################################################

######################################################################
# Support functions:

#--------------------------------------------------------------------#
def cdata(string):
    cdata_string="<![CDATA["+string+"]]>"
    return cdata_string
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def uidstr(guid):
    uid_string=" uid="+"\""+guid+"\""
    return uid_string
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def cidstr(guid):
    uid_string=" cid="+"\""+guid+"\""
    return uid_string
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def pidstr(guid):
    pid_string=" pid="+"\""+guid+"\""
    return pid_string
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def urlparticipa(prefix, guid):
    http_str="http://participatorio.juventude.gov.br/"
    url_participa=http_str+prefix+guid
    return url_participa
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def hrefstr(url):
    href_string=" href="+"\""+url+"\""
    return href_string
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def datestr(time):
    if time != '':
        date=str(datetime.datetime.fromtimestamp(int(time)))
    else:
        date=''
    return date
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def post_content(db, post_guid, content_typeid):
    content = db.cursor()
    content.execute(qry_post_content, (post_guid, content_typeid,))
    if content.rowcount == 1:
        post_content = content.fetchone()[0]
    else:
        post_content=''
        print "ERRO! Nenhum ou Mais do que um resultado para a query"
        
    content.close()
    
    return post_content
#--------------------------------------------------------------------#

######################################################################

######################################################################
# Functions that write on XML file

#--------------------------------------------------------------------#
def write_tag (xml, level, tag_name, info_str, attr_str):
    if len(info_str) > 0:
        tag_begin=("<"+tag_name+attr_str+">")
        tag_end=("</"+tag_name+">")
        xml.write(level+tag_begin+info_str+tag_end+"\n")
    else:
        xml.write(level+"<"+tag_name+attr_str+"/>"+"\n")
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_comments (db, xml, post_guid):
    post_comments = db.cursor()
    post_comments.execute(qry_post_comments, (post_guid,))
    
    xml.write(l4+"<comentarios>\n")
    for (user_id, user_name, user_username, string, time) in post_comments:
        
        xml.write(l5+"<comentario>\n")
        
        user_attr=uidstr(urlparticipa('profile/',user_username))
        write_tag(xml,l6,"usuario",user_name,user_attr)
        write_tag(xml,l6,"data",datestr(time),'')
        write_tag(xml,l6,"mensagem",cdata(string),'')
        
        xml.write(l5+"</comentario>\n")
        
    xml.write(l4+"</comentarios>\n")
    
    post_comments.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_userfriends_subsection (db, xml, user_guid):
    friends_info = db.cursor()
    friends_info.execute(qry_user_friends, (user_guid))
    
    xml.write(l2+"<amigos>\n")
    for (friend_id, friend_name, friend_username) in friends_info:
        friend_attr=uidstr(urlparticipa('profile/',friend_username))
        write_tag(xml,l3,"usuario",friend_name,friend_attr)
    xml.write(l2+"</amigos>\n")
        
    friends_info.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_userowngroup_subsection (db, xml, user_guid):        
    user_owngroups = db.cursor()
    user_owngroups.execute(qry_user_owngroups, (user_guid, user_guid, ))
        
    xml.write(l3+"<dono>\n")
    for (group_id, group_title) in user_owngroups:
        group_attr=cidstr(urlparticipa('groups/profile/',str(group_id)))
        write_tag(xml,l4,"comunidade",group_title,group_attr)
    xml.write(l3+"</dono>\n")
        
    user_owngroups.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_usermembergroup_subsection (db, xml, user_guid):
    user_membergroups = db.cursor()
    user_membergroups.execute(qry_user_membergroups, (user_guid, ))
        
    xml.write(l3+"<membro>\n")
    for (group_id, group_title) in user_membergroups:
        group_attr=cidstr(urlparticipa('groups/profile/',str(group_id)))
        write_tag(xml,l4,"comunidade",group_title,group_attr)
    xml.write(l3+"</membro>\n")
        
    user_membergroups.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_usergroups_subsection (db, xml, user_guid):
    xml.write(l2+"<comunidades>\n")
    write_userowngroup_subsection(db, xml, user_guid)
    write_usermembergroup_subsection(db, xml, user_guid)
    xml.write(l2+"</comunidades>\n")
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_userfiles_subsection (db, xml, user_guid):
    user_files = db.cursor()
    
    # 1 = select * from elgg_entity_subtypes where subtype='file';
    user_files.execute(qry_user_posts, (user_guid, user_guid, 1,))
    
    xml.write(l2+"<arquivos>\n")
    
    for (post_guid, post_title, post_desc, time)\
        in user_files:
                    
        link_prefix="http://participatorio.juventude.gov.br/file/download/"
        file_link=str(link_prefix)+str(post_guid)
        
        post_attr=pidstr(urlparticipa('file/view/',str(post_guid)))
        xml.write(l3+"<arquivo"+post_attr+">\n")
        
        write_tag(xml,l4,"titulo",post_title,'')
        write_tag(xml,l4,"data",datestr(time),'')
        write_tag(xml,l4,"link",'',hrefstr(file_link))
        write_tag(xml,l4,"descricao",cdata(post_desc),'')
            
        write_comments(db,xml,post_guid)
        
        xml.write(l3+"</arquivo>\n")
    
    xml.write(l2+"</arquivos>\n")
    user_files.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_userblogs_subsection (db, xml, user_guid):
    user_blogs = db.cursor()
    
    # 4 = select * from elgg_entity_subtypes where subtype='blog';
    user_blogs.execute(qry_user_posts, (user_guid, user_guid, 4,))
    
    xml.write(l2+"<blogs>\n")
    
    for (post_guid, post_title, post_desc, time)\
        in user_blogs:
                    
        post_excerpt = db.cursor()
        
        # 64 = select * from elgg_metastrings where string='excerpt';
        post_excerpt=post_content(db,post_guid,64)
            
        post_attr=pidstr(urlparticipa('blog/view/',str(post_guid)))
        xml.write(l3+"<blog"+post_attr+">\n")

        write_tag(xml,l4,"titulo",post_title,'')
        write_tag(xml,l4,"data",datestr(time),'')
        write_tag(xml,l4,"resumo",cdata(post_excerpt),'')
        write_tag(xml,l4,"texto",cdata(post_desc),'')
                    
        write_comments(db,xml,post_guid)
        
        xml.write(l3+"</blog>\n")
            
    xml.write(l2+"</blogs>\n")
    
    user_blogs.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_userbookmarks_subsection (db, xml, user_guid):
    user_bookmarks = db.cursor()
    
    # 13 = select * from elgg_entity_subtypes where subtype='bookmarks';
    user_bookmarks.execute(qry_user_posts, (user_guid, user_guid, 13,))
    
    xml.write(l2+"<favoritos>\n")
    
    for (post_guid, post_title, post_desc, time)\
        in user_bookmarks:
                    
        # 90 = select * from elgg_metastrings where string='address';
        bookmark_link=post_content(db,post_guid,90)
  
        post_attr=pidstr(urlparticipa('bookmarks/view/',str(post_guid)))
        xml.write(l3+"<favorito"+post_attr+">\n")
    
        write_tag(xml,l4,"titulo",post_title,'')
        write_tag(xml,l4,"data",datestr(time),'')
        write_tag(xml,l4,"link",'',hrefstr(bookmark_link))
        write_tag(xml,l4,"descricao",cdata(post_desc),'')
                    
        write_comments(db,xml,post_guid)
        
        xml.write(l3+"</favorito>\n")
                
    xml.write(l2+"</favoritos>\n")
    
    user_bookmarks.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#    
def write_userpages_subsection (db, xml, user_guid):
    user_pages = db.cursor()
    
    # 14 = select * from elgg_entity_subtypes where subtype='page_top';
    user_pages.execute(qry_user_posts, (user_guid, user_guid, 14,))
    
    xml.write(l2+"<paginas>\n")
    
    for (post_guid, post_title, post_desc, time)\
        in user_pages:
        
        post_attr=pidstr(urlparticipa('pages/view/',str(post_guid)))
        xml.write(l3+"<pagina"+post_attr+">\n")

        write_tag(xml,l4,"titulo",post_title,'')
        write_tag(xml,l4,"data",datestr(time),'')
        write_tag(xml,l4,"texto",cdata(post_desc),'')
                    
        write_comments(db,xml,post_guid)
        
        xml.write(l3+"</pagina>\n")
        
    xml.write(l2+"</paginas>\n")
    
    user_pages.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_uservideos_subsection (db, xml, user_guid):
    user_videos = db.cursor()
    
    # 12 = select * from elgg_entity_subtypes where subtype='videos';
    user_videos.execute(qry_user_posts, (user_guid, user_guid, 12,))
    
    xml.write(l2+"<videos>\n")
    
    for (post_guid, post_title, post_desc, time)\
        in user_videos:
                    
        # 477 = select * from elgg_metastrings where string='video_url';
        video_link=post_content(db, post_guid, 477)
        
        post_attr=pidstr(urlparticipa('videos/view/',str(post_guid)))
        xml.write(l3+"<video"+post_attr+">\n")
        
        write_tag(xml,l4,"titulo",post_title,'')
        write_tag(xml,l4,"data",datestr(time),'')
        write_tag(xml,l4,"link",'',hrefstr(video_link))
        write_tag(xml,l4,"descricao",cdata(post_desc),'')
        
        write_comments(db,xml,post_guid)
        
        xml.write(l3+"</video>\n")
        
    xml.write(l2+"</videos>\n")
    
    user_videos.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_userevents_subsection (db, xml, user_guid):
    user_events = db.cursor()
    
    # 6 = select * from elgg_entity_subtypes where subtype='calendar_event';
    user_events.execute(qry_user_posts, (user_guid, user_guid, 6,))
    
    
    xml.write(l2+"<eventos>\n")
    
    for (post_guid, post_title, post_desc, time)\
        in user_events:
            
        # 18 = select * from elgg_metastrings where string='venue';
        venue=post_content(db, post_guid, 18)
        
        # 20 = select * from elgg_metastrings where string='start_date';
        time_start=post_content(db, post_guid, 20)

        # 22 = select * from elgg_metastrings where string='end_date';
        time_end=post_content(db, post_guid, 22)
        
        # 26 = select * from elgg_metastrings where string='fees';
        fees=post_content(db, post_guid, 26)
        
        # 28 = select * from elgg_metastrings where string='contact';
        contact=post_content(db, post_guid, 28)
        
        # 30 = select * from elgg_metastrings where string='organizer';
        organizer=post_content(db, post_guid, 30)
        
        post_attr=pidstr(urlparticipa('event_calendar/view/',str(post_guid)))
        xml.write(l3+"<evento"+post_attr+">\n")
        
        write_tag(xml,l4,"titulo",post_title,'')
        write_tag(xml,l4,"data",datestr(time),'')
        write_tag(xml,l4,"organizador",organizer,'')
        write_tag(xml,l4,"contato",contact,'')
        write_tag(xml,l4,"endereco",venue,'')
        write_tag(xml,l4,"data_inicio",datestr(time_start),'')
        write_tag(xml,l4,"data_fim",datestr(time_end),'')
        write_tag(xml,l4,"taxa_participacao",fees,'')
        write_tag(xml,l4,"descricao",cdata(post_desc),'')
        
        write_comments(db,xml,post_guid)
        
        xml.write(l3+"</evento>\n")
    
    xml.write(l2+"</eventos>\n")
    
    user_events.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#    
def write_users_section (db, xml_file):
    
    xml = codecs.open(xml_file,'w',encoding='utf-8')
    
    xml.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")

    xml.write("<usuarios>\n")
    
    users_info = db.cursor()
    users_info.execute(qry_users_info)
    
    for (guid, name, username) in users_info:
        
        user_attr=uidstr(urlparticipa('profile/',username))
        xml.write(l1+"<usuario"+user_attr+">\n")
        
        # Write all user's information
        write_tag(xml,l2,"nome",name,'')
            
        # Write a list of user friend's names
        write_userfriends_subsection(db, xml, guid)
        
        # Write a list of all groups that the user owns or belongs
        write_usergroups_subsection(db, xml, guid)
        
        # Write a list, and all the info, of all posts made by the user
        write_userfiles_subsection(db, xml, guid)
        write_userblogs_subsection(db, xml, guid)
        write_userbookmarks_subsection(db, xml, guid)
        write_userpages_subsection(db, xml, guid)
        write_uservideos_subsection(db, xml, guid)
        write_userevents_subsection(db, xml, guid)
        
        xml.write(l1+"</usuario>\n")
    
    xml.write("</usuarios>\n")
    
    users_info.close()
    
    xml.close()
#--------------------------------------------------------------------#

######################################################################
