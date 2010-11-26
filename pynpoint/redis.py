"""
   Copyright 2010 Christopher MacGown

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
""" pynpoint redis client """

from __future__ import absolute_import
import redis as pyredis
from pynpoint.config import Config


class Redis(object):
    """ A Borg-style wrapper for Redis client class. """
    __shared_state = {}

    def __new__(cls, config=Config()):
        self = object.__new__(cls)
        self.__dict__ = cls.__shared_state
        return self

    def __init__(self, config=Config()):
        if not self.__dict__:
            print "Opening a new redis connection"
            kwargs = {"host": config.redis_hostname,
                      "port": config.redis_port,
                      "db": config.redis_db}

            self.conn = pyredis.Redis(**kwargs)

    def __getattr__(self, name):
        def call(*args, **kwargs):
            """ Pass through the query to our redis connection """
            cmd = getattr(self.conn, name)
            return cmd(*args, **kwargs)

        if name in self.__dict__:
            return self.__dict__.get(name)

        return call
