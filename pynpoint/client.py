"""
   Copyright 2010 Christopher MacGown

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
""" The pynpoint gossip discovery client """

import eventlet

from pynpoint import config, protocol


class ClientError(Exception):
    """ A client error class """
    pass


class Client(object):
    """ A pynpoint client """
    _config = config.Config()

    def __init__(self, host=_config.server_hostname, port=_config.server_port):
        self.socket = eventlet.connect((host, port))

    def recv(self):
        """ recv data back from connection """
        return self.socket.recv(1024)

    def send(self, data):
        """ send data to server """
        if not type(data) == protocol.Packet:
            raise ClientError

        self.socket.sendall(data.encode())
