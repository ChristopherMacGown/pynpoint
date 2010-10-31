""" pynpoint redis client """

import pyredis
from pynpoint.config import Config


class Redis(pyredis.Redis):
    """ A Borg-style Redis client class. """
    __shared_state = {}

    def __new__(cls):
        self = object.__new__(cls)
        self.__dict__ = cls.__shared_state
        return self

    def __init__(self, config=Config()):
        if not self.__dict__:
            print "Opening a new redis connection"
            kwargs = {"host": config.redis_hostname,
                      "port": config.redis_port,
                      "db": config.redis_db}

            pyredis.Redis.__init__(self, **kwargs)
