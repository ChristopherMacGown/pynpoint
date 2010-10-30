import json
import struct

SIZE_PACK_FORMAT = ">H"
VERSION_PACK_FORMAT = ">B"

# PROTOCOL STUFF
VERSION = 0x01
HEADER_IDENTIFIER = 'pnpt'
HEADER_DELIMITER = "|"
BODY_DELIMITER = "\n"
TERMINATOR = "!!"


class ProtocolError(Exception):
    """ A generic protocol error class """
    # TODO(chris): Handle logging here.
    pass


class Packet(object):
    """ A pynpoint packet """

    def __init__(self, request_type, payload):
        self.request_type = request_type
        self.payload = payload
        self.size = len(self.request_type) + len(self.body()) + 1

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
        packet = packet.rstrip()[0:-len(TERMINATOR)]

        header_id, version, size, req_and_body = packet.split(HEADER_DELIMITER)
        try:
            header_id, version, size, req_and_body = packet.split(HEADER_DELIMITER)

            if header_id == HEADER_IDENTIFIER and \
               struct.unpack(SIZE_PACK_FORMAT, size)[0] == len(req_and_body):
                #TODO(chris): handle validation
                req, body = req_and_body.split('\n')
                body = json.JSONDecoder().decode(body)
                return Packet(req, body)


        except (ValueError, ProtocolError):
            raise ProtocolError, "invalid packet: %s" % packet
