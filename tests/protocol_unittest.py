""" Protocol tests """

import unittest
from json import JSONEncoder, JSONDecoder
from pynpoint import config, protocol, redis
from pynpoint.protocol import handlers
from tests import common


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
        self.export = protocol.Packet('i have', {"stuff": 2})
        self.query = protocol.Packet("heard of?", {"type": 'addresses',
                                                   "value": '123.45.67.8'})

    def test_get_packet_handler(self):
        expected_handlers = [handlers.Announcement,
                             handlers.Export,
                             handlers.Query]

        actual_handlers = [protocol.get_packet_handler(x) for x in
                           (self.announcement, self.export, self.query)]

        self.assertRaises(protocol.ProtocolError, 
                          protocol.get_packet_handler, 
                          protocol.Packet('wrong_packet', {}))

        for ex, ac in zip(expected_handlers, actual_handlers):
            self.assertEqual(ex, ac)

    def test_validate_export(self):
        validator = handlers.Query._validate_payload
        # No way to assertNothingRaised
        self.assertEqual(None, validator(self.query.payload))

        # Validator raises on invalid payload
        self.assertRaises(handlers.RequestError, validator, None)
        self.assertRaises(handlers.RequestError, validator, [])
        self.assertRaises(handlers.RequestError, validator, "")
        self.assertRaises(handlers.RequestError, validator, {})


    def test_validate_announcement(self):
        validator = handlers.Announcement._validate_payload
        # No way to assertNothingRaised
        self.assertEqual(None, validator(self.announcement.payload))

        # Validator raises on invalid payload
        self.assertRaises(handlers.RequestError, validator, None)
        self.assertRaises(handlers.RequestError, validator, [])
        self.assertRaises(handlers.RequestError, validator, "")
        self.assertRaises(handlers.RequestError, validator, {})

    def test_handle_announcement(self):
        self.assertTrue(protocol.handle_packet(self.announcement))


    def test_validate_query(self):
        validator = handlers.Query._validate_payload
        # No way to assertNothingRaised
        self.assertEqual(None, validator(self.query.payload))

        # Validator raises on invalid payload
        self.assertRaises(handlers.RequestError, validator, None)
        self.assertRaises(handlers.RequestError, validator, [])
        self.assertRaises(handlers.RequestError, validator, "")
        self.assertRaises(handlers.RequestError, validator, {})

    def test_handle_query(self):
        self.assertTrue(protocol.handle_packet(self.query))
        self.assertEqual(protocol.handle_packet(self.query), [self.test_host])
