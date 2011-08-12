import unittest

import platform

from pynpoint import exc

import pynpoint.providers as providers
import pynpoint.providers.darwin


class ProvidersTestCase(unittest.TestCase):
    def setUp(self):
        self.old_platform_system = platform.system

    def tearDown(self):
        platform.platform = self.old_platform_system

    def test_load_providers(self):
        def fake_platform_system(*args, **kwargs):
            return "Darwin"

        platform.system = fake_platform_system
        self.assertEqual([providers.darwin], providers.load_providers())
