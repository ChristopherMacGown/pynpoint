import json


HEADER_DELIMITER = ":"
BODY_DELIMITER = "\n"

class PynpointEncoder(object):
    @classmethod
    def encode(cls, request_type, payload):
        def header(request_type, size):
            return HEADER_DELIMITER.join(('pnpt', VERSION, size, request_type)

        request_size = len(request_type) + len(payload) + 1
        return BODY_DELIMITER.join(header(request_type, request_size), payload)


class PynpointDecoder(object):
    @classmethod
    def decode(cls, request):
        pass
