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
# Return: All group instances, and its info, from database.
qry_groups_info = \
("	SELECT g.guid, g.name, g.description, \
        u.guid, u.name, u.username, e.time_created \
	FROM elgg_entities e, elgg_groups_entity g, elgg_users_entity u\
	WHERE e.guid = g.guid AND e.owner_guid = u.guid \
    AND (e.access_id = 1 OR e.access_id = 2) \
    ORDER BY e.time_created ASC; ")
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
# Argument: Group_ID / InfoType_ID
# Return: All InfoTypes' posts from this group.
qry_group_posts = \
("	SELECT o.guid, o.title, o.description, \
        u.guid, u.name, u.username, e.time_created\
	FROM elgg_entities e, elgg_objects_entity o, elgg_users_entity u\
	WHERE e.guid = o.guid AND e.owner_guid = u.guid\
    AND (e.access_id = 1 OR e.access_id = 2) \
    AND e.container_guid = %s AND e.subtype = %s \
    ORDER BY e.time_created ASC; ")
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
# Argument: Group_ID
# Return: Flag containing the access control to become a group member
qry_group_access_permission = \
("  SELECT CASE WHEN s.string = '2' THEN 'public' ELSE 'private' END \
    FROM elgg_metadata d, elgg_metastrings s \
    WHERE d.value_id = s.id \
    AND d.entity_guid = %s AND d.name_id = %s; ")
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
# Argument: Group_ID / InfoType_ID
# Return: Yes or No, depending on the permission given by the owner.
qry_post_content_permission = \
("  SELECT CASE WHEN s.string = 'yes' THEN 'Sim' ELSE 'Nao' END \
    FROM elgg_metadata d, elgg_metastrings s \
    WHERE d.value_id = s.id \
    AND d.entity_guid = %s AND d.name_id = %s;")
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
# Argument: Group_ID
# Return: All members' name from this group.
qry_group_members = \
("  SELECT u.guid, u.name, u.username \
    FROM elgg_users_entity u, elgg_entity_relationships r \
    WHERE u.guid = r.guid_one \
    AND r.relationship = 'member' AND r.guid_two = %s; ")
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
def permstr(perm):
    perm_string=" habilitado="+"\""+str(perm)+"\""
    return perm_string
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def qtystr(quantity):
    qty_string=" quantidade="+"\""+str(quantity)+"\""
    return qty_string
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

#--------------------------------------------------------------------#
def postcontent_permission (db, group_guid, content_id):
        
    perm = db.cursor()
    perm.execute(qry_post_content_permission, (group_guid, content_id,))

    if perm.rowcount == 1:
       permission=perm.fetchone()[0]
    else:
        permission=''
        print "ERRO! Nenhum ou Mais do que um resultado para a query"
    
    perm.close()
    
    return permission        
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def groupaccess_permission (db, group_guid):
        
    access = db.cursor()
    
    # 55 = select * from elgg_metastrings where string = 'membership';
    access.execute(qry_group_access_permission, (group_guid, 55,))

    if access.rowcount == 1:
       access_control=access.fetchone()[0]
    else:
        access_control=''
        print "ERRO! Nenhum ou Mais do que um resultado para a query"
    
    access.close()
    
    return access_control        
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

#-------------------------------------------------------------------#
def write_groupmembers_subsection (db, xml, group_guid):
    group_members = db.cursor()
    group_members.execute(qry_group_members, (group_guid,))
    
    write_tag(xml,l2,"quantidade_membros",str(group_members.rowcount),'')
                    
    xml.write(l2+"<membros>\n")
    for (user_id, user_name, user_username) in group_members:
        user_attr=uidstr(urlparticipa('profile/',user_username))
        write_tag(xml,l3,"usuario",user_name,user_attr)
    xml.write(l2+"</membros>\n")
    
    group_members.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_groupfiles_subsection (db, xml, group_guid):
    group_files = db.cursor()
    
    # 1 = select * from elgg_entity_subtypes where subtype='file';
    group_files.execute(qry_group_posts, (group_guid, 1,))
    
    # 50 = select * from elgg_metastrings where string='file_enable';
    perm=postcontent_permission(db, group_guid, 50)
    
    xml.write(l2+"<arquivos"+permstr(perm)+">\n")
    
    for (post_guid, post_title, post_desc, \
            owner_id, owner_name, owner_username, time)\
        in group_files:
        
        link_prefix="http://participatorio.juventude.gov.br/file/download/"
        file_link=str(link_prefix)+str(post_guid)
        
        post_attr=pidstr(urlparticipa('file/view/',str(post_guid)))
        xml.write(l3+"<arquivo"+post_attr+">\n")

        owner_attr=uidstr(urlparticipa('profile/',owner_username))
        write_tag(xml,l4,"autor",owner_name,owner_attr)
        write_tag(xml,l4,"titulo",post_title,'')
        write_tag(xml,l4,"data",datestr(time),'')
        write_tag(xml,l4,"link",'',hrefstr(file_link))
        write_tag(xml,l4,"descricao",cdata(post_desc),'')
                    
        write_comments(db,xml,post_guid)
        
        xml.write(l3+"</arquivo>\n")
        
    xml.write(l2+"</arquivos>\n")
    
    group_files.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_groupforumtopics_subsection (db, xml, group_guid):
    group_forumtopics = db.cursor()
    
    # 7 = select * from elgg_entity_subtypes where subtype='groupforumtopic';
    group_forumtopics.execute(qry_group_posts, (group_guid, 7,))
    
    # 52 = select * from elgg_metastrings where string='forum_enable';
    perm=postcontent_permission(db, group_guid, 52)
    
    xml.write(l2+"<debates"+permstr(perm)+">\n")
    
    for (post_guid, post_title, post_desc, \
        owner_id, owner_name, owner_username, time)\
        in group_forumtopics:
        
        post_attr=pidstr(urlparticipa('discussion/view/',str(post_guid)))
        xml.write(l3+"<debate"+post_attr+">\n")

        owner_attr=uidstr(urlparticipa('profile/',owner_username))
        write_tag(xml,l4,"autor",owner_name,owner_attr)
        write_tag(xml,l4,"titulo",post_title,'')
        write_tag(xml,l4,"data",datestr(time),'')
        write_tag(xml,l4,"texto",cdata(post_desc),'')
            
        write_comments(db,xml,post_guid)
        
        xml.write(l3+"</debate>\n")
        
    xml.write(l2+"</debates>\n")
    
    group_forumtopics.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_groupbookmarks_subsection (db, xml, group_guid):
    group_bookmarks = db.cursor()
    
    # 13 = select * from elgg_entity_subtypes where subtype='bookmarks';
    group_bookmarks.execute(qry_group_posts, (group_guid, 13,))
    
    # 49 = select * from elgg_metastrings where string='bookmarks_enable';
    perm=postcontent_permission(db, group_guid, 49)
    
    xml.write(l2+"<favoritos"+permstr(perm)+">\n")
    
    for (post_guid, post_title, post_desc, \
            owner_id, owner_name, owner_username, time)\
        in group_bookmarks:
            
        # 90 = select * from elgg_metastrings where string='address';
        bookmark_link=post_content(db,post_guid,90)
        
        post_attr=pidstr(urlparticipa('bookmarks/view/',str(post_guid)))
        xml.write(l3+"<favorito"+post_attr+">\n")

        owner_attr=uidstr(urlparticipa('profile/',owner_username))
        write_tag(xml,l4,"autor",owner_name,owner_attr)
        write_tag(xml,l4,"titulo",post_title,'')
        write_tag(xml,l4,"data",datestr(time),'')
        write_tag(xml,l4,"link",'',hrefstr(bookmark_link))
        write_tag(xml,l4,"descricao",cdata(post_desc),'')
                            
        write_comments(db,xml,post_guid)
        
        xml.write(l3+"</favorito>\n")
    
    xml.write(l2+"</favoritos>\n")
    
    group_bookmarks.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_grouppages_subsection (db, xml, group_guid):
    group_pages = db.cursor()
    
    # 14 = select * from elgg_entity_subtypes where subtype='page_top';
    group_pages.execute(qry_group_posts, (group_guid, 14,))
    
    # 53 = select * from elgg_metastrings where string='pages_enable';
    perm=postcontent_permission(db, group_guid, 53)
    
    xml.write(l2+"<paginas"+permstr(perm)+">\n")
    
    for (post_guid, post_title, post_desc,
            owner_id, owner_name, owner_username, time)\
        in group_pages:
            
        post_attr=pidstr(urlparticipa('pages/view/',str(post_guid)))
        xml.write(l3+"<pagina"+post_attr+">\n")

        owner_attr=uidstr(urlparticipa('profile/',owner_username))
        write_tag(xml,l4,"autor",owner_name,owner_attr)
        write_tag(xml,l4,"titulo",post_title,'')
        write_tag(xml,l4,"data",datestr(time),'')
        write_tag(xml,l4,"texto",cdata(post_desc),'')
                    
        write_comments(db,xml,post_guid)
        
        xml.write(l3+"</pagina>\n")
        
    xml.write(l2+"</paginas>\n")
    
    group_pages.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_groupvideos_subsection (db, xml, group_guid):
    group_videos = db.cursor()
    
    # 12 = select * from elgg_entity_subtypes where subtype='videos';
    group_videos.execute(qry_group_posts, (group_guid, 12,))
    
    # 399 = select * from elgg_metastrings where string='videos_enable';
    perm=postcontent_permission(db, group_guid, 399)
    
    xml.write(l2+"<videos"+permstr(perm)+">\n")
    
    for (post_guid, post_title, post_desc, \
            owner_id, owner_name, owner_username, time)\
        in group_videos:
            
        # 477 = select * from elgg_metastrings where string='video_url';
        video_link=post_content(db,post_guid, 477)
            
        post_attr=pidstr(urlparticipa('videos/view/',str(post_guid)))
        xml.write(l3+"<video"+post_attr+">\n")

        owner_attr=uidstr(urlparticipa('profile/',owner_username))
        write_tag(xml,l4,"autor",owner_name,owner_attr)
        write_tag(xml,l4,"titulo",post_title,'')
        write_tag(xml,l4,"data",datestr(time),'')
        write_tag(xml,l4,"link",'',hrefstr(video_link))
        write_tag(xml,l4,"descricao",cdata(post_desc),'')
            
        write_comments(db,xml,post_guid)
        
        xml.write(l3+"</video>\n")
        
    xml.write(l2+"</videos>\n")
    
    group_videos.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_groupevents_subsection (db, xml, group_guid):
    group_events = db.cursor()
    
    # 6 = select * from elgg_entity_subtypes where subtype='calendar_event';
    group_events.execute(qry_group_posts, (group_guid, 6,))
    
    # 54 = select * from elgg_metastrings where string='event_calendar_enable';
    perm=postcontent_permission(db, group_guid, 54)
    
    xml.write(l2+"<eventos"+permstr(perm)+">\n")
    
    for (post_guid, post_title, post_desc, \
            owner_id, owner_name, owner_username, time)\
        in group_events:
            
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
        
        owner_attr=uidstr(urlparticipa('profile/',owner_username))
        write_tag(xml,l4,"autor",owner_name,owner_attr)
        write_tag(xml,l4,"titulo",post_title,'')
        write_tag(xml,l4,"data",datestr(time),'')
        write_tag(xml,l4,"organizador",organizer,'')
        write_tag(xml,l4,"contato",contact,'')
        write_tag(xml,l4,"endereco",venue,'')
        write_tag(xml,l4,"data_inicio",datestr(time_start),'')
        write_tag(xml,l4,"data_fim",datestr(time_end),'')
        write_tag(xml,l4,"taxa_participacao",fees,'')
        write_tag(xml,l4,"descricao",cdata(post_desc),'')
        
        xml.write(l3+"</evento>\n")
        
        write_comments(db,xml,post_guid)
    
    xml.write(l2+"</eventos>\n")
    
    group_events.close()
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
def write_groups_section(db, xml_file):

    xml = codecs.open(xml_file,'w',encoding='utf-8')
    
    xml.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")

    xml.write("<comunidades>\n")
    
    groups_info = db.cursor()
    groups_info.execute(qry_groups_info)
    
    for (guid, title, desc, owner_id, owner_name, owner_username, time)\
        in groups_info:
        
        # 45 = select * from elgg_metastrings where string='briefdescription';
        brief_desc=post_content(db,guid, 45)
        
        group_attr=cidstr(urlparticipa('groups/profile/',str(guid)))
        xml.write(l1+"<comunidade"+group_attr+">\n")

        # Write all group's information
        owner_attr=uidstr(urlparticipa('profile/',owner_username))
        write_tag(xml,l2,"proprietario",owner_name,owner_attr)
        write_tag(xml,l2,"titulo",title,'')
        write_tag(xml,l2,"data",datestr(time),'')
        write_tag(xml,l2,"descricao",cdata(desc),'')
        write_tag(xml,l2,"breve_descricao",cdata(brief_desc),'')
                                    
        if groupaccess_permission(db, guid) == 'public':
            
            # Write a list of group member's name
            write_groupmembers_subsection(db, xml, guid)
        
            # Write a list, and all the info, of all posts made on the group.
            write_groupfiles_subsection(db, xml, guid)
            write_groupforumtopics_subsection(db, xml, guid)
            write_groupbookmarks_subsection(db, xml, guid)
            write_grouppages_subsection(db, xml, guid)
            write_groupvideos_subsection(db, xml, guid)
            write_groupevents_subsection(db, xml, guid)
        
        xml.write(l1+"</comunidade>\n")
        
    xml.write("</comunidades>\n")
    
    groups_info.close()
    
    xml.close()
#--------------------------------------------------------------------#

######################################################################
