import argparse
import logging
from abc import ABC, abstractmethod
from typing import Dict, List

import playwright
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

from vfs_appointment_bot.utils.config_reader import get_config_value


class VfsBot(ABC):
    """
    Abstract base class for VfsBot

    Provides common functionalities like login, pre-login steps, appointment checking, and notification.
    Subclasses are responsible for implementing country-specific login and appointment checking logic.
    """

    def __init__(self):
        """
        Initializes a VfsBot instance for a specific country.

        """
        self.country_code = None
        self.appointment_param_keys: List[str] = []

    def run(self, args: argparse.Namespace = None) -> None:
        """
        Starts the VFS bot for appointment checking and notification.

        This method reads configuration values, performs login, checks for
        appointments based on provided arguments, and sends notifications if
        appointments are found.

        Args:
            args (argparse.Namespace, optional): Namespace object containing parsed
                command-line arguments. Defaults to None.
        """

        logging.info(f"Starting VFS Bot for {self.country_code}")

        # Configuration values
        try:
            browser_type = get_config_value("browser", "type", "firefox")
            vfs_url = get_config_value("vfs-url", self.country_code)
        except KeyError as e:
            logging.error(f"Missing configuration value: {e}")
            return

        email_id = get_config_value("vfs-credential", "email")
        password = get_config_value("vfs-credential", "password")

        appointment_params = self.get_appointment_params(args)

        # Launch browser and perform actions
        with sync_playwright() as p:
            browser = getattr(p, browser_type).launch(headless=False)
            page = browser.new_page()
            stealth_sync(page)

            page.goto(vfs_url)
            self.pre_login_steps(page)

            try:
                self.login(page, email_id, password)
                logging.info("Logged in successfully")
            except Exception as e:
                logging.error(f"Login failed: {e}")
                browser.close()
                return

            logging.info(f"Checking appointments for {appointment_params}")
            dates = self.check_for_appontment(page, appointment_params)
            if dates:
                # Log successful appointment finding
                logging.info(f"Found appointments on: {', '.join(dates)}")
                self.notify_appointment(dates)
            else:
                # Log no appointments found
                logging.info("No appointments found for the specified criteria.")

            browser.close()

    def get_appointment_params(self, args: argparse.Namespace) -> Dict[str, str]:
        """
        Collects appointment parameters from command-line arguments or user input.

        This method iterates through pre-defined `appointment_param_keys` (replace
        with relevant keys) and retrieves values either from provided arguments
        or prompts the user for input if values are missing.

        Args:
            args (argparse.Namespace): Namespace object containing parsed command-line arguments.

        Returns:
            Dict[str, str]: A dictionary containing appointment parameters.
        """
        appointment_params = {}
        for key in self.appointment_param_keys:
            if (
                getattr(args, "appointment_params") is not None
                and args.appointment_params[key] is not None
            ):
                appointment_params[key] = args.appointment_params[key]
            else:
                key_name = key.replace("_", " ")
                appointment_params[key] = input(f"Enter the {key_name}: ")
        return appointment_params

    @abstractmethod
    def login(
        self, page: playwright.sync_api.Page, email_id: str, password: str
    ) -> None:
        """
        Performs login steps specific to the VFS website for the bot's country.

        This abstract method needs to be implemented by subclasses to handle
        country-specific login procedures (e.g., filling login form elements, handling
        CAPTCHAs). It should interact with the Playwright `page` object to achieve
        login functionality.

        Args:
            page (playwright.sync_api.Page): The Playwright page object used for browser interaction.
            email_id (str): The user's email address for VFS login.
            password (str): The user's password for VFS login.

        Raises:
            Exception: If login fails due to unexpected errors.
        """
        raise NotImplementedError("Subclasses must implement login logic")

    @abstractmethod
    def pre_login_steps(self, page: playwright.sync_api.Page) -> None:
        """
        Performs any pre-login steps required by the VFS website for the bot's country.

        This abstract method allows subclasses to implement country-specific actions
        that need to be done before login (e.g., cookie acceptance, language selection).
        It should interact with the Playwright `page` object to perform these actions.

        Args:
            page (playwright.sync_api.Page): The Playwright page object used for browser interaction.
        """
        pass  # Subclasses can implement optional pre-login steps

    @abstractmethod
    def check_for_appontment(
        self, page: playwright.sync_api.Page, appointment_params: Dict[str, str]
    ) -> List[str]:
        """
        Checks for appointments based on provided parameters on the VFS website.

        This abstract method needs to be implemented by subclasses to interact with
        the VFS website and search for appointments based on the given `appointment_params`
        dictionary. It should use the Playwright `page` object to navigate the website
        and extract appointment dates.

        Args:
            page (playwright.sync_api.Page): The Playwright page object used for browser interaction.
            appointment_params (Dict[str, str]): A dictionary containing appointment search criteria.

        Returns:
            List[str]: A list of available appointment dates (empty list if none found).
        """
        raise NotImplementedError(
            "Subclasses must implement appointment checking logic"
        )