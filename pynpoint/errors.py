class RequestError(Exception):
    """ Common exception for Request Handlers """
    pass


class ProtocolError(Exception):
    """ A generic protocol error class """
    # TODO(chris): Handle logging here.
    pass
