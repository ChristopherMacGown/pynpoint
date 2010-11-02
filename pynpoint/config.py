# -*- coding: utf-8 -*-
""" pynpoint config singleton """

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

    __default_configs = ("pynpoint.cfg",        # Sane Defaults
                         "/etc/pynpoint.cfg",   # Site level configs
                         "~/.pynpoint.cfg")     # Are we running as a user?
    __shared_state = {}

    def __new__(cls, config_files=__default_configs):
        self = object.__new__(cls)
        self.__dict__ = cls.__shared_state
        return self

    def __init__(self, config_files=__default_configs):
        if not self.__dict__:
            print "Assimilating your biological distinctiveness"
            for config_file in config_files:
                self._parse_config_file(config_file)

            if not self.__dict__:
                raise ConfigError("Didn't find configuration files, bailing.")

    def __getattr__(self, item):
        if item in self.__dict__:
            return self[item]
        else:
            return None

    def __parse_config_yaml(self, cfg):
        try:
            import yaml
            return yaml.load(cfg) # Returns None which sucks.
        except yaml.ParserError as e:
            raise ValueError(e.args)

    def __parse_config_json(self, cfg):
        import json
        return json.JSONDecoder().decode(cfg)

    def _parse_config_file(self, config_file):
        """ Parses a configuration file as a dict and populates __dict__
        with them. __dict__ is Config.__shared_state
        """

        parsers = (self.__parse_config_json, self.__parse_config_yaml)

        try:
            with open(config_file) as fp:
                cfg = fp.read()

                for parser in parsers:
                    try:
                        config = parser(cfg)
                    except (ValueError, ImportError):
                        pass

                for (section_name, section) in config.items():
                    for (item, value) in section.items():
                        config_attr = "%s_%s" % (section_name, item)
                        self.__setattr__(config_attr, value)
        except (AttributeError, TypeError, IOError):
            pass
