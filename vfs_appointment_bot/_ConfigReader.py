import logging

from configparser import ConfigParser

class _ConfigReader:
    
    def __init__(self):
        self.config_object = ConfigParser()
        self.config_object.read("config/config.ini")

    def read_prop(self, section_header, prop_name):
        value = self.config_object.get(section_header,prop_name)
        logging.debug("{}:{}".format(prop_name, value))
        return value

    def read_bool_prop(self, section_header, prop_name):
        value = self.config_object.getboolean(section_header,prop_name)
        logging.debug("{}:{}".format(prop_name, value))
        return value