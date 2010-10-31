""" Pynpoint request handlers """


class RequestHandler(object):
    """ Request Handler class """

    # TODO(chris): Move diffie-hellman, json into here.
    def __init__(self, payload):
        self.body = payload


class Announcement(RequestHandler):
    """ Announcement handler """
    pass


class Export(RequestHandler):
    """ Export handler """
    pass


class Query(RequestHandler):
    """ Query handler """
    pass
