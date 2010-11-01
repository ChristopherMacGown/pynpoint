import unittest
import os
from pynpoint.config import Config, ConfigError
from tests import common

class ConfigTestCase(unittest.TestCase):
    _test_good_config_file = "tests/data/good.cfg"
    _test_bad_config_file = "tests/data/bad.cfg"

    def setUp(self):
        common.reset_config()
    
    def test_that_json_parsing_works(self):
        config = Config(config_files=[self._test_good_config_file])
        self.assertTrue(config.test_attribute)
        self.assertFalse(config.test_false_attribute)

    def test_raises_config_error_on_bad_parse(self):
        self.assertRaises(ConfigError, Config, config_files=[None])
        self.assertRaises(ConfigError, Config, 
                          config_files=[self._test_bad_config_file])
