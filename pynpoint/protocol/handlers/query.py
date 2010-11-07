# pylint: disable-msg=E1101,E1102,W0232,R0801

""" Mixin for Query type packet handler """

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
            assert payload['type']
            assert payload['type'] in valid_payload_types
        except AssertionError:
            raise RequestError("Invalid payload: %s" % payload)

        return fn(self, **kwargs)
    return validator

class Query:
    """ Query handler """


    @validate
    def execute(self, host=None):
        """ Handle an inbound query """
        key, value = self.packet.payload['type'], self.packet.payload['value']

        result = []
        for host in self._r.keys(pattern="host_*"):
            host = json.JSONDecoder().decode(self._r.get(host))

            query_values = host.get(key, None)
            if query_values:
                if value in query_values:
                    result.append(host)

        return result

Mixin.register("heard of?", Query)
