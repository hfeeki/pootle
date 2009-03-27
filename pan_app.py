#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Zuza Software Foundation
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

from threading import Lock

from django.conf import settings
from django.utils.translation import ugettext

from translate.misc.context import with_
from translate.misc.contextlib import contextmanager

from pootle_app.lib import prefs as prefsmodule

cache_templates = True

prefs = prefsmodule.load_preferences(settings.PREFSFILE)

# Contains an instance of PootleServer. Eventually we'll
# move all the code out of PootleServer and its superclasses
# and then this object can be removed. It's safe to share this
# object, since it contains no state.
pootle_server = None

def get_default_language():
    return settings.LANGUAGE_CODE
