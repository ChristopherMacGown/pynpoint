""" Protocol tests """

import unittest
from pynpoint import config, protocol
from pynpoint.protocol import handlers
from tests import common


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


class ProtocolHandlersTestCase(unittest.TestCase):
    """ Protocol Handler Test cases """

    def setUp(self):
        common.reset_config()
        config.Config()

        self.announcement = protocol.Packet('hi!', {'host': '123.45.67.89'})
        self.export = protocol.Packet('i have', {"stuff": 2})
        self.query = protocol.Packet("heard of?", {"something": 1})

    def test_get_packet_handler(self):
        expected_handlers = [ handlers.Announcement,
                              handlers.Export,
                              handlers.Query ]

        actual_handlers = [protocol.get_packet_handler(x) for x in 
                           (self.announcement, self.export, self.query)]

        for ex, ac in zip(expected_handlers, actual_handlers):
            self.assertEqual(ex, ac)

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
        handler = protocol.get_packet_handler(self.announcement)
        self.assertTrue(handler.handle(self.announcement.payload))




