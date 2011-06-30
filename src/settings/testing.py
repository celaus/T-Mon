##############################################################################
#
# Copyright (c) 2011 Reality Jockey Ltd. and Contributors.
# This file is part of TMon.
#
# TMon is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TMon is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with django-tornado. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

# -*- coding: utf-8 -*-

__docformat__ = "reStructuredText"

from settings import *
from os import path

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/claus/sandbox/rjdj.tmon/db/tmon_testing.db',
        },
    }
    
TRACKING_DATABASE = {
    'protocol': 'http',
    'url': 'localhost',
    'port': 5984,
    'name': 'tracking_data',
    'user': 'admin',
    'password': 'admin',
    }

LOGFILE = path.join(BASE_DIR, "..", "testing.log")
LOGLEVEL = "debug"
