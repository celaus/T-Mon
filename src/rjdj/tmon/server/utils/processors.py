##############################################################################
#
# Copyright (c) 2011 Reality Jockey Ltd. and Contributors.
# This file is part of T-Mon.
#
# T-Mon is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# T-Mon is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with T-Mon. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

# -*- coding: utf-8 -*-

__docformat__ = "reStructuredText"

from rjdj.tmon.server.exceptions import *
from rjdj.tmon.server.couchdbviews.couchdbkeys import CouchDBKeys as Keys
from rjdj.tmon.server.models import TrackingData
from rjdj.tmon.server.utils import location
from threading import Thread
from Queue import Queue
import time
import logging

logger = logging.getLogger("debug")

class FieldProcessor(object):
    """ """
    
    def __init__(self, queue = None):
        """ """
 
        self.queue = queue

    def to_queue(self, fieldname, decrypted_data):
        """ """
        
        try:
            self.queue.put(self.process(fieldname, decrypted_data))
        except Exception as ex: 
            logger.info("%s: %s" % (fieldname, ex))
        
            
class RequiredFieldProcessor(FieldProcessor):
    """ """
    
    def process(self, fieldname, decrypted_data):
        
        value = decrypted_data.get(fieldname)
        if not value: raise FieldMissing(fieldname)
        
        return { fieldname : value }
    
class OptionalFieldProcessor(FieldProcessor):
    """ """
    
    def process(self, fieldname, decrypted_data):
    
        value = decrypted_data.get(fieldname)
        return value and { fieldname : value } or {}
        
    
class IPProcessor(RequiredFieldProcessor):
    """ """
    
    COUNTRY_KEY = Keys.COUNTRY
    CITY_KEY = Keys.CITY
    LATITUDE_KEY = Keys.LATITUDE
    LONGITUDE_KEY = Keys.LONGITUDE
    
    
    def process(self, fieldname, decrypted_data):
    
        ip = super(IPProcessor, self).process(fieldname, decrypted_data)

        if not ip: 
            return {}

        result = ip
        
        user_location = ip and location.resolve(ip[fieldname]) or None
        
        country = None
        city = None
        latitude = None
        longitude = None
        
        if user_location:
            # some (127.0.0.0, 10.0.0.0, 192.168.0.0 or other) IP addresses could result in None
            result[self.COUNTRY_KEY] = user_location["country"]
            result[self.CITY_KEY] = user_location["city"]
            result[self.LATITUDE_KEY] = user_location["latitude"]
            result[self.LONGITUDE_KEY] = user_location["longitude"]
        
        return result
      
        
def process(decrypted_data):
    """ """

    results = Queue()
    processors = {
        Keys.IP: IPProcessor(results),
        Keys.USER_AGENT: RequiredFieldProcessor(results),
        Keys.USERNAME: OptionalFieldProcessor(results),
        Keys.URL: RequiredFieldProcessor(results)
    }
    
    threads = []
    for k, p in processors.iteritems():
        t = Thread(target = p.to_queue, args = (k, decrypted_data))
        t.start()
        threads.append(t)
    
    for t in threads: t.join()
    
    result_dict = { Keys.TIMESTAMP: TrackingData.now() }
    while not results.empty():
        result_dict.update(results.get())
    
    return result_dict