#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2009 Zuza Software Foundation
# 
# This file is part of translate.
#
# translate is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# translate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with translate; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from django.db import connection

def get_latest_changes(manager, query):
    cursor = connection.cursor()
    cursor.execute(query)
    return dict(cursor.fetchall())

def table_name(table):
    return table._meta.db_table

def field_name(table, field_name):
    return '%s.%s' % (table_name(table), table._meta.get_field(field_name).column)

def primary_key_name(table):
    return field_name(table, table._meta.pk.name)
