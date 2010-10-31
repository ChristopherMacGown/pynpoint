"""
The pynpoint gossip protocol listener
"""

import eventlet
import logging

from pynpoint import config, protocol


class CloseSession(Exception):
    """ Closes the connection """
    pass


class FriendlyConnection(object):
    """ An inbound connection with message """

    def __init__(self, sock_address, server):
        self.socket, self.address = sock_address
        self.server = server

    def loop(self):
        """ Get the data """

        while True:
            if not self.handle_inbound():
                return False

    def handle_inbound(self):
        """
            Handles inbound data, if it's a Packet decodes it, otherwise
            closes the connection
        """
        try:
            # Grab all of the data on the wire, and create a protocol.Packet
            # out of it.
            # TODO(chris): Improve performance by reading each field as it
            #              comes across the wire.
            packet = ""
            terminator_pos = -1 * len(protocol.TERMINATOR)
            while True:
                if len(packet) > 1 and \
                   packet.rstrip()[terminator_pos:] == protocol.TERMINATOR:
                    break

                packet = packet + self.socket.recv(1024)

            print packet
            packet = protocol.Packet.decode(packet)
            print packet
            return True
        except CloseSession:
            return False


class Server(object):
    """
    The pydislocated gossip protocol listener
    """

    _config = config.Config()

    def __init__(self, host=_config.server_hostname, port=_config.server_port):
        """ Initialize everything """

        self.host = host
        self.port = port
        self.socket = None
        self.logger = logging.getLogger('server.log')

    def run(self):
        """ Run the listener """

        self.socket = eventlet.listen((self.host, self.port))
        self.logger.info("listening on %s:%s" % (self.host, self.port))

        try:
            while True:
                eventlet.spawn_n(self.handle_inbound, self.socket.accept())
        except KeyboardInterrupt:
            return True

    def handle_inbound(self, address):
        """ Loops over the messages coming from the client """
        FriendlyConnection(address, self).loop()
