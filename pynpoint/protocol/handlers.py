""" Pynpoint request handlers """

from pynpoint.redis import Redis
from pynpoint.config import Config

class RequestError(Exception):
    """ Common exception for Request Handlers """


class RequestHandler(object):
    """ Request Handler class """

    _config = Config()
    _r = Redis()

    @classmethod
    def handle(cls, payload, host=None):
        cls._validate_payload(payload)

        if not host: 
            try:
                host = payload['host']
            except KeyError:
                raise RequestError("Invalid payload: %s" % payload)

        key = 'host_%s' % host
        return cls._store(key, payload)

    @classmethod
    def _validate_payload(cls, payload):
        try:
            print payload
            assert type(payload) == dict
            assert len(payload) > 0
        except AssertionError:
            raise RequestError("Invalid payload: %s" % payload)

    @classmethod
    def _store(cls, key, payload):
        """ Store the value in Redis """
        ttl = payload.pop('ttl', cls._config.default_ttl)

        return cls._r.setex(key, payload, ttl)


class Announcement(RequestHandler):
    """ Announcement handler """

    @classmethod
    def _validate_payload(cls, payload):
        RequestHandler._validate_payload(payload)
        assert payload['host']
        # TODO(chris): Validate that there exists a DH key init value


class Export(RequestHandler):
    """ Export handler """
    pass


class Query(RequestHandler):
    """ Query handler """
    pass
