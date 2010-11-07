""" Protocol tests """

import unittest
from json import JSONEncoder, JSONDecoder
from tests import common

from pynpoint import config, protocol, redis
from pynpoint.errors import ProtocolError, RequestError
from pynpoint.mixins import Mixin
from pynpoint.protocol import handlers
from pynpoint.protocol.handlers import announcement, export, query


class ProtocolTestCase(unittest.TestCase):
    """ Protocol tests """

    def setUp(self):
        self.packet = protocol.Packet('test', {'test': 'data'})
        self.packet_dup = protocol.Packet('test', {'test': 'data'})

    def test_packet_encode(self):
        self.assertEqual('pnpt|\x01|\x00\x00\x00\x15|test\n{"test": "data"}!!',
                         self.packet.encode())

    def test_packet_decode(self):
        decoder = protocol.Packet.decode
        self.assertEqual(self.packet, decoder(self.packet.encode()))

        bad_packets = ['pnpt|\x01|\x00\x00\x00|test\n{"test": "data"}!!',
                       'pnpt|foo']

        for bad_packet in bad_packets:
            self.assertRaises(protocol.ProtocolError, decoder, bad_packet)

    def test_packet_equality(self):
        self.assertTrue(self.packet == self.packet_dup)
        self.assertFalse(self.packet is self.packet_dup)
        self.assertFalse(self.packet == None)



class ProtocolHandlersTestCase(unittest.TestCase):
    """ Protocol Handler Test cases """

    def setUp(self):
        common.reset_config()
        config.Config()


        self.test_host = {"host": "127.0.0.1", 
                          "port": 9999,
                          "addresses": ["123.45.67.8"]}

        r = redis.Redis()
        r.setex('host_123.45.67.8', JSONEncoder().encode(self.test_host), 10)


        self.announcement = protocol.Packet('hi!', {'host': '123.45.67.89'})
        self.export = protocol.Packet('i have', {'host': '123.45.67.89', 
                                                 "type": 'addresses',
                                                 'export':["123.45.67.89"]})
        self.query = protocol.Packet("heard of?", {"type": 'addresses',
                                                   "value": '123.45.67.8'})

    def bad_data(self, request_type):
        bd = [None, [], "", {}]
        return [protocol.Packet(request_type, d) for d in bd]

    def test_handle_export(self):
        handler = protocol.handle_packet
        self.assertTrue(handler(self.export))

        # Validator raises on invalid payload
        for bad_packet in self.bad_data('i have'):
            self.assertRaises(RequestError, handler, bad_packet)

    def test_handle_announcement(self):
        handler = protocol.handle_packet
        self.assertTrue(handler(self.announcement))


        # Validator raises on invalid payload
        for bad_packet in self.bad_data('hi!'):
            self.assertRaises(RequestError, handler, bad_packet)

    def test_handle_query(self):
        handler = protocol.handle_packet
        self.assertTrue(handler(self.query))
        self.assertEqual(handler(self.query), [self.test_host])

        # Validator raises on invalid payload
        for bad_packet in self.bad_data('heard of?'):
            self.assertRaises(RequestError, handler, bad_packet)
