""" Pynpoint request handlers """

import json
from pynpoint.redis import Redis
from pynpoint.config import Config


class RequestError(Exception):
    """ Common exception for Request Handlers """


class RequestHandler(object):
    """ Request Handler class """

    _config = Config()
    _r = Redis()

    @classmethod
    def _validate_payload(cls, payload):
        """ Validates the payload """
        try:
            assert type(payload) == dict
            assert len(payload) > 0
        except AssertionError:
            raise RequestError("Invalid payload: %s" % payload)

    @classmethod
    def _store(cls, key, payload):
        """ Store the value in Redis """
        ttl = payload.pop('ttl', cls._config.default_ttl)
        payload = json.JSONEncoder().encode(payload)

        return cls._r.setex(key, payload, ttl)


class Announcement(RequestHandler):
    """ Announcement handler """

    @classmethod
    def handle(cls, payload, host=None):
        """ Handle a hello """
        cls._validate_payload(payload)

        if not host:
            host = payload['host']

        key = 'host_%s' % host
        return cls._store(key, payload)

    @classmethod
    def _validate_payload(cls, payload):
        """ Validates the payload """
        RequestHandler._validate_payload(payload)
        assert payload['host']
        # TODO(chris): Validate that there exists a DH key init value


class Export(RequestHandler):
    """ Export handler """
    pass


class Query(RequestHandler):
    """ Query handler """

    @classmethod
    def handle(cls, payload, host=None):
        """ Handle an inbound query """

        cls._validate_payload(payload)
        query_key = payload['type']
        query_value = payload['value']

        result = []
        for host in cls._r.keys(pattern="host_*"):
            host = json.JSONDecoder().decode(cls._r.get(host))

            query_values = host.get(query_key, None)
            if query_values:
                if query_value in query_values:
                    result.append(host)

        if result:
            return result

    @classmethod
    def _validate_payload(cls, payload):
        """ Validates the payload """
        RequestHandler._validate_payload(payload)
        assert payload['type'] 
        assert payload['type'] in ("hosts", "services", "addresses", "disks")
