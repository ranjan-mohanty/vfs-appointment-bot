import os
from configparser import ConfigParser
from typing import Dict

_config = None


def get_config_parser(config_dir="config"):
    """
    Reads all INI configuration files in a directory and caches the result.

    Args:
        config_dir: The directory containing configuration files (default: "config").

    Returns:
        A ConfigParser object loaded with configuration data.
    """
    global _config
    if not _config:
        _config = ConfigParser()
        for entry in os.scandir(config_dir):
            if entry.is_file() and entry.name.endswith(".ini"):
                config_file_path = os.path.join(config_dir, entry.name)
                _config.read(config_file_path)
    return _config


def get_config_section(section: str, default: Dict = None) -> Dict:
    """
    Get a configuration section as a dictionary.

    Args:
        section: The name of the section to retrieve.
        default: A dictionary containing default values for the section (optional).

    Returns:
        A dictionary containing the configuration for the specified section,
        or the provided default dictionary if the section is not found.
    """
    config = get_config_parser()
    if config.has_section(section):
        return dict(config[section])
    else:
        return default or {}


def get_config_value(section: str, key: str, default: str = None) -> str:
    """
    Get a specific configuration value.

    Args:
        section: The name of the section containing the value.
        key: The name of the key to retrieve.
        default: The default value to return if the section or key is not found (optional).

    Returns:
        The value associated with the given key within the specified section,
        or the provided default value if the section or key does not exist.
    """
    config = get_config_parser()
    if config.has_section(section) and config.has_option(section, key):
        return config[section][key]
    else:
        return default
