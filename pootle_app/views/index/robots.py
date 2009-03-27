#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Zuza Software Foundation
#
# This file is part of Pootle.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

from django.http import HttpResponse
from pootle_app.models import Language

def view(request):
    """generates the robots.txt file"""
    langcodes = [language.code for language in Language.objects.all()]
    excludedfiles = ["login.html", "register.html", "activate.html"]
    content = "User-agent: *\n"
    for excludedfile in excludedfiles:
        content += "Disallow: /%s\n" % excludedfile
    for langcode in langcodes:
        content += "Disallow: /%s/\n" % langcode
    return HttpResponse(content, mimetype="text/plain")