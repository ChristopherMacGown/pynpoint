"""
Defines the pynpoint protocol with a Packet handler.
"""


import json
import struct
from pynpoint.errors import ProtocolError
from pynpoint.protocol import handlers

SIZE_PACK_FORMAT = ">I"
VERSION_PACK_FORMAT = ">B"

# PROTOCOL STUFF
VERSION = 0x01
HEADER_IDENTIFIER = 'pnpt'
HEADER_DELIMITER = "|"
BODY_DELIMITER = "\n"
TERMINATOR = "!!"

SUPPORTED_VERSIONS = [VERSION]


def handle_packet(packet):
    """ Call the appropriate handler for our packet """

    handler = handlers.RequestHandler(packet)
    return handler.handle()


class Packet(object):
    """ A pynpoint packet """

    def __init__(self, request_type, payload):
        self.request_type = request_type
        self.payload = payload
        self.size = len(self.request_type) + len(self.body()) + 1

    def __eq__(self, other):
        if type(other) == Packet and \
           self.payload == other.payload and \
           self.request_type == other.request_type:
            return True

        return False

    def encode(self):
        """ Encodes a packet """
        return BODY_DELIMITER.join((self.header(), self.body())) + TERMINATOR

    def header(self):
        """ Returns a packet header """

        size = struct.pack(SIZE_PACK_FORMAT, self.size)
        version = struct.pack(VERSION_PACK_FORMAT, VERSION)
        _header = (HEADER_IDENTIFIER, version, size, self.request_type)
        return HEADER_DELIMITER.join(_header)

    def body(self):
        """ Returns json encoded payload """
        return json.JSONEncoder().encode(self.payload)

    @classmethod
    def decode(cls, packet):
        """ Takes a string and attempts to decode it as a pynpoint packet """

        # Strip the packet terminator
        packet = packet.rstrip()[0:-len(TERMINATOR)]

        try:
            header, version, sz, req_and_body = packet.split(HEADER_DELIMITER)

            version = struct.unpack(VERSION_PACK_FORMAT, version)[0]
            size = struct.unpack(SIZE_PACK_FORMAT, sz)[0]

            if header == HEADER_IDENTIFIER and \
               version in SUPPORTED_VERSIONS and \
               size == len(req_and_body):
                #TODO(chris): handle validation
                req, body = req_and_body.split('\n')
                body = json.JSONDecoder().decode(body)
                return Packet(req, body)

        except (struct.error, ValueError, ProtocolError):
            raise ProtocolError("invalid packet: %s" % packet)
