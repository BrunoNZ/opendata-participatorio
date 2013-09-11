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

######################################################################
# Users Section Query definitions:

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

######################################################################

######################################################################
# Group Section Query definitions:

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
# Argument: Group_ID
# Return: All members' name from this group.
qry_group_members = \
("  SELECT u.guid, u.name, u.username \
    FROM elgg_users_entity u, elgg_entity_relationships r \
    WHERE u.guid = r.guid_one \
    AND r.relationship = 'member' AND r.guid_two = %s; ")
#--------------------------------------------------------------------#
    
######################################################################

######################################################################

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
