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
