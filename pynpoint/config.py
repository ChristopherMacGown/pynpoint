# -*- coding: utf-8 -*-
""" pynpoint config singleton """

import json


# TODO(chris): Turn this into an array of expected locations for configurations
#              /etc/pynpoint.cfg, ~/.pynpoint.cfg, ./pynpoint.cfg (for dev)
DEFAULT_CONFIG_FILE = "pynpoint.cfg"

# TODO(chris): Create a default config dict… oh! Put it in __shared_state so
#              the Config() object auto initializes with sane defaults.

DEFAULT_CONFIG_DICT = {}


class ConfigError(Exception):
    """ A config error """
    pass


class Config(object):
    """ Borg style Config object, the shared state is only initialized once.
    All configuration options are set as properties on this object with in
    the format of sectionname_key.

    For example:
       {"server": {"hostname": "somehost"}} -> Config().server_hostname
    """

    __shared_state = {}

    def __new__(cls, config_file=DEFAULT_CONFIG_FILE):
        self = object.__new__(cls)
        self.__dict__ = cls.__shared_state
        return self

    def __init__(self, config_file=DEFAULT_CONFIG_FILE):
        if not self.__dict__:
            print "Assimilating your biological distinctiveness"
            self._parse_config_file(config_file)

    def __getattr__(self, item):
        if item in self.__dict__:
            return self[item]
        else:
            return None

    def _parse_config_file(self, config_file):
        """ Parses a configuration file as a dict and populates __dict__
        with them. __dict__ is Config.__shared_state
        """

        try:
            with open(config_file) as fp:
                cfg = fp.read()
                config = json.JSONDecoder().decode(cfg)

                for (section_name, section) in config.items():
                    for (item, value) in section.items():
                        config_attr = "%s_%s" % (section_name, item)
                        self.__setattr__(config_attr, value)
        except (IOError, TypeError, ValueError) as e:
            raise ConfigError(e.args)
