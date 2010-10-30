""" The pynpoint gossip discovery client """

import eventlet

from pynpoint import config
from pynpoint import protocol


class ClientError(Exception):
    """ A client error class """
    pass


class Client(object):
    """ A pynpoint client """

    def __init__(self, host=config.HOSTNAME, port=config.PORT):
        self.socket = eventlet.connect((host, port))

    def recv(self):
        """ recv data back from connection """
        return self.socket.recv(1024)

    def send(self, data):
        """ send data to server """
        if not type(data) == protocol.Packet:
            raise ClientError

        self.socket.sendall(data.encode())
