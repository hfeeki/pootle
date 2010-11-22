#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2008-2009 Zuza Software Foundation
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

import traceback
import sys

from django.utils import simplejson

from django.core.exceptions import PermissionDenied
from django.http import  HttpResponseForbidden, HttpResponseServerError
from django.http import Http404, HttpResponse
from django.template.loader import render_to_string
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.conf import settings
from django.core.mail import mail_admins

from pootle_misc.baseurl import l

class ErrorPagesMiddleware(object):
    """
    Friendlier Error Pages
    """
    def _ajax_error(self, rcode, msg):
        json = {'msg': msg}
        response = simplejson.dumps(json)
        return HttpResponse(response, status=rcode, mimetype="application/json")

    def process_exception(self, request, exception):
        msg = unicode(exception)
        if isinstance(exception, Http404):
            if request.is_ajax():
                return self._ajax_error(404, msg)

        elif isinstance(exception, PermissionDenied):
            if request.is_ajax():
                return self._ajax_error(403, msg)

            templatevars = {}
            templatevars['permission_error'] = msg
            if not request.user.is_authenticated():
                login_msg = _('You need to <a href="%(login_link)s">login</a> to access this page.',
                              {'login_link': l("/accounts/login/")})
                templatevars["login_message"] = login_msg
            return HttpResponseForbidden(render_to_string('403.html', templatevars,
                                      RequestContext(request)))

        else:
            #FIXME: implement better 500
            tb = traceback.format_exc()
            print >> sys.stderr, tb
            if not settings.DEBUG:
                try:
                    templatevars = {}
                    templatevars['exception'] = msg
                    if hasattr(exception, 'filename'):
                        msg = _('Error accessing %(filename)s, Filesystem sent error: %(errormsg)s',
                                                    {'filename': exception.filename, 'errormsg': exception.strerror})
                        templatevars['fserror'] = msg
                    # send email to admins with details about exception
                    subject = 'Error (%s IP): %s' % ((request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS and 'internal' or 'EXTERNAL'), request.path)
                    try:
                        request_repr = repr(request)
                    except:
                        request_repr = "Request repr() unavailable"
                    message = "%s\n\n%s\n\n%s" % (unicode(exception.args[0]), tb, request_repr)
                    mail_admins(subject, message, fail_silently=True)

                    if request.is_ajax():
                        return self._ajax_error(500, msg)
                    return HttpResponseServerError(render_to_string('500.html', templatevars,
                                                                    RequestContext(request)))
                except:
                    # let's not confuse things by throwing an exception here
                    pass
