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
