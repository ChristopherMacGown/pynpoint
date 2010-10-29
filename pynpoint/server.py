import config
import eventlet
import logging

"""
The pydislocate gossip protocol listener
"""


class FriendlyConnection(object):
    def __init__(self, sock_address, server):
        self.socket, self.address = sock_address
        self.server = server

    def loop(self):
        """ Get the data """

        while True:
            if not self.handle_inbound():
                return False

    def handle_inbound(self):
        try:
            raw_data = self.socket
            print raw_data.recv(1024)

        except CloseSession:
            return False


class Server(object):
    """
    The pydislocated gossip protocol listener
    """


    def __init__(self, host=config.hostname, port=config.port):
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
        FriendlyConnection(address, self).loop()




