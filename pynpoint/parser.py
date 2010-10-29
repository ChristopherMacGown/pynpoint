import json

VERSION = 0x01
HEADER_IDENTIFIER = 'pnpt'
HEADER_DELIMITER = ":"
BODY_DELIMITER = "\n"

class PynpointEncodeError(Exception):
    pass


class PynpointDecodeError(Exception):
    pass


class PynpointEncoder(object):
    @classmethod
    def encode(cls, request_type, payload):
        def header(request_type, size):
            _header = (HEADER_IDENTIFIER, str(VERSION), str(size), request_type)
            return HEADER_DELIMITER.join(_header)

        try:
            request_size = len(request_type) + len(payload) + 1
            _header = header(request_type, request_size)
            return BODY_DELIMITER.join((_header, payload))
        except Exception(e):
            raise PynpointEncoderError(e)


class PynpointDecoder(object):
    @classmethod
    def decode(cls, request):
        def parse_header(header):
            #TODO(chris) handle validation of the request here.
            identifier, version, size, request = header.split(HEADER_DELIMITER)
            return request

        def validate_body(request, body):
            #TODO(chris): Create validate body methods and validate body.
            return True

        header, body = request.split(BODY_DELIMITER)

        body = json.JSONDecoder().decode(body)
        request = parse_header(header)

        if validate_body(request, body):
            return body
