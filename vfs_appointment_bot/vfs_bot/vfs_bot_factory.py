import logging
from importlib import import_module

from vfs_appointment_bot.vfs_bot.vfs_bot import VfsBot

COUNTRY_BOT_MAP = {"de": "VfsBotDe"}


class UnsupportedCountryError(Exception):
    """Raised when an unsupported country code is provided."""

    pass


def get_vfs_bot(source_country_code: str, destination_country_code: str) -> VfsBot:
    """Retrieves the appropriate VfsBot class for a given country.

    This function searches for a matching subclass of `VfsBot` based on the
    provided destination country code (ISO 3166-1 alpha-2).
    If no matching class is found, an `UnsupportedCountryError` exception is raised.

    Args:
        source_country_code (str): The ISO 3166-1 alpha-2 country code where you're applying from.
        destination_country_code (str): The ISO 3166-1 alpha-2 country code where the appointment is needed.

    Returns:
        VfsBot: An instance of the `VfsBot` subclass specific to the provided country.

    Raises:
        UnsupportedCountryError: If the provided country is not supported.
    """

    country_lower = destination_country_code.lower()

    if country_lower in COUNTRY_BOT_MAP:
        bot_class_name = COUNTRY_BOT_MAP[country_lower]
        bot_module = import_module(
            f"vfs_appointment_bot.vfs_bot.vfs_bot_{country_lower}"
        )
        bot_class = getattr(bot_module, bot_class_name)
        return bot_class(source_country_code)
    else:
        raise UnsupportedCountryError(
            f"Country {destination_country_code} is not supported"
        )
