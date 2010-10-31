""" Protocol tests """

import unittest
from pynpoint import protocol

class ProtocolTestCase(unittest.TestCase):
    """ Protocol tests """

    def setUp(self):
        self.packet = protocol.Packet('test', {'test': 'data'})

    def test_packet_encode(self):
        self.assertEqual('pnpt|\x01|\x00\x00\x00\x15|test\n{"test": "data"}!!', 
                         self.packet.encode())

    def test_packet_decode(self):
        self.assertEqual(self.packet, 
                         protocol.Packet.decode(self.packet.encode()))
