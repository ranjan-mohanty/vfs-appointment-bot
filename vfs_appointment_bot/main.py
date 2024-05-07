import argparse
import logging
import sys
from typing import Dict

from vfs_appointment_bot.utils.config_reader import get_config_value, initialize_config
from vfs_appointment_bot.utils.timer import countdown
from vfs_appointment_bot.vfs_bot.vfs_bot import LoginError
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
    initialize_config()

    parser = argparse.ArgumentParser(
        description="VFS Appointment Bot: Checks for appointments at VFS Global"
    )
    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument(
        "-sc",
        "--source-country-code",
        type=str,
        help="The ISO 3166-1 alpha-2 source country code (refer to README)",
        metavar="<country_code>",
        required=True,
    )

    required_args.add_argument(
        "-dc",
        "--destination-country-code",
        type=str,
        help="The ISO 3166-1 alpha-2 destination country code (refer to README)",
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
    source_country_code = args.source_country_code
    destination_country_code = args.destination_country_code
    try:
        while True:
            vfs_bot = get_vfs_bot(source_country_code, destination_country_code)
            appointment_found = vfs_bot.run(args)
            if appointment_found:
                break
            countdown(
                int(get_config_value("default", "interval")),
                "Next appointment check in",
            )

    except (UnsupportedCountryError, LoginError) as e:
        logging.error(e)
    except Exception as e:
        logging.exception(e)


def initialize_logger():
    file_handler = logging.FileHandler("app.log", mode="a")
    file_handler.setFormatter(
        logging.Formatter(
            "[%(asctime)s] %(levelname)s [%(filename)s:%(lineno)d] %(message)s"
        )
    )

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter("[%(asctime)s] %(message)s"))
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s [%(filename)s:%(lineno)d] %(message)s",
        handlers=[
            file_handler,
            stream_handler,
        ],
    )


if __name__ == "__main__":
    main()
