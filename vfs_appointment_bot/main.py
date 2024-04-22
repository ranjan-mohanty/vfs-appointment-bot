import argparse
import logging
from configparser import ConfigParser
from logging.config import fileConfig
import sys
from typing import Dict

from vfs_appointment_bot.utils.timer import countdown
from vfs_appointment_bot.vfs_bot.vfs_bot_factory import (
    UnsupportedCountryError,
    get_vfs_bot,
)


class KeyValueAction(argparse.Action):
    """Custom action class for parsing appointment parameters.

    This class handles parsing comma-separated key-value pairs provided through
    the `--appointment-params` argument. It ensures the format is valid (key=value)
    and stores the parsed parameters as a dictionary.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        try:
            appointment_params: Dict[str, str] = {
                key.strip(): value.strip()
                for key, value in (item.split("=") for item in values.split(","))
            }
            setattr(namespace, "appointment_params", appointment_params)
        except ValueError:
            parser.error(
                f"Invalid value format for {option_string}, use key=value pairs"
            )


def main() -> None:
    """
    Entry point for the VFS Appointment Bot.

    This function sets up logging, parses command-line arguments, and runs the VFS appointment
    checking process in a continuous loop. It catches exceptions for unsupported countries and
    unexpected errors, logging them appropriately.

    Raises:
        UnsupportedCountryError: If the provided country code is not supported by the bot.
        Exception: For any other unexpected errors encountered during execution.
    """
    initialize_logger()

    parser = argparse.ArgumentParser(
        description="VFS Appointment Bot: Checks for appointments at VFS Global"
    )
    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument(
        "-c",
        "--country-code",
        type=str,
        help="The ISO 3166-1 alpha-2 country code (refer to README)",
        metavar="<country_code>",
        required=True,
    )

    parser.add_argument(
        "-ap",
        "--appointment-params",
        type=str,
        default=None,
        help="Comma-separated key-value pairs for additional appointment details (refer to VFS website)",
        action=KeyValueAction,
        metavar="<key1=value1,key2=value2,...>",
    )

    args = parser.parse_args()
    country_code = args.country_code
    try:
        while True:
            vfs_bot = get_vfs_bot(country_code)
            vfs_bot.run(args)
            countdown(120)  # Wait 2 minutes before next execution

    except UnsupportedCountryError as e:
        logging.error(e)
    except Exception as e:
        logging.exception(e)


def initialize_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s [%(filename)s:%(lineno)d] %(message)s",
        handlers=[
            logging.FileHandler("app.log", mode="a"),
            logging.StreamHandler(sys.stdout),
        ],
    )


if __name__ == "__main__":
    main()