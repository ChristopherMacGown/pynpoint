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
        def call(*args):
            """ Pass through the query to our redis connection """
            cmd = getattr(self.conn, name)
            return cmd(*args)

        if name in self.__dict__:
            return self.__dict__.get(name)

        return call
