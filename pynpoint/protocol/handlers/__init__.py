""" Pynpoint request handlers """

import json
from pynpoint.mixins import Mixin
from pynpoint.redis import Redis
from pynpoint.config import Config
from pynpoint.protocol.handlers import announcement, query, export


class RequestHandler(object):
    """ Request Handler class """

    _config = Config()
    _r = Redis()

    def __init__(self, packet):
        self.packet = packet

    def default_validator(self):
        assert type(self.packet.payload) == dict
        assert len(self.packet.payload) > 0

    def handle(self):
        mixin = Mixin.get_mixin(self.packet.request_type)

        with Mixin(self, mixin) as handler:
            # handler.execute is really self, with mixin mixed in.
            return handler.execute()

    def _store(self, key, payload):
        """ Store the value in Redis """
        ttl = payload.pop('ttl', self._config.default_ttl)
        payload = json.JSONEncoder().encode(payload)

        return self._r.setex(key, payload, ttl)
