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
# pylint: disable-msg=E1101,E1102,W0232

""" Mixin for Export type packet handler """

import json

from pynpoint.errors import RequestError
from pynpoint.mixins import Mixin


def validate(fn):
    """ Validation decorator """
    def validator(self, **kwargs):
        """ Validates a packet"""
        payload = self.packet.payload
        try:
            valid_payload_types = ('hosts', 'services', 'addresses', 'disks')
            self.default_validator()
            print payload
            assert payload['type']
            assert payload['type'] in valid_payload_types
            assert type(payload['export']) == list
            assert len(payload['export']) > 0
        except AssertionError:
            raise RequestError("Invalid payload: %s" % payload)

        return fn(self, **kwargs)
    return validator


class Export:
    """ Export handler """

    @validate
    def execute(self, host=None):
        """ handle an inbound export """
        if not host:
            host = self.packet.payload['host']

        key = 'host_%s' % host
        return self._store(key, self.packet.payload)

Mixin.register("i have", Export)
