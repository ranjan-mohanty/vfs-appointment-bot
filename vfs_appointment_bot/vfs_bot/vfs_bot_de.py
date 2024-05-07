import logging
from typing import Dict, List, Optional

from playwright.sync_api import Page

from vfs_appointment_bot.utils.date_utils import extract_date_from_string
from vfs_appointment_bot.vfs_bot.vfs_bot import VfsBot


class VfsBotDe(VfsBot):
    """Concrete implementation of VfsBot for Germany (DE).

    This class inherits from the base `VfsBot` class and implements
    country-specific logic for interacting with the VFS website for Germany.
    It overrides the following methods to handle German website specifics:

    - `login`: Fills the login form elements with email and password.
    - `pre_login_steps`: Rejects all cookie policies if presented.
    - `check_for_appontment`: Performs appointment search based on provided
        parameters and extracts available dates from the website.
    """

    def __init__(self, source_country_code: str):
        """
        Initializes a VfsBotDe instance for Germany.

        This constructor sets the source country code and the destination country
        code "de"(Germany). It also defines appointment parameter keys specific
        to the destination country's VFS website.

        Args:
            source_country_code (str): The country code where you're applying from.
        """
        super().__init__()
        self.source_country_code = source_country_code
        self.destination_country_code = "DE"
        self.appointment_param_keys = [
            "visa_center",
            "visa_category",
            "visa_sub_category",
        ]

    def login(self, page: Page, email_id: str, password: str) -> None:
        """
        Performs login steps specific to the German VFS website.

        This method fills the email and password input fields on the login form
        and clicks the "Sign In" button. It raises an exception if the login fails
        (e.g., if the "Start New Booking" button is not found after login).

        Args:
            page (playwright.sync_api.Page): The Playwright page object used for browser interaction.
            email_id (str): The user's email address for VFS login.
            password (str): The user's password for VFS login.

        Raises:
            Exception: If login fails due to unexpected errors or missing "Start New Booking" button.
        """
        email_input = page.locator("#mat-input-0")
        password_input = page.locator("#mat-input-1")

        email_input.fill(email_id)
        password_input.fill(password)

        page.get_by_role("button", name="Sign In").click()
        page.wait_for_selector("role=button >> text=Start New Booking")

    def pre_login_steps(self, page: Page) -> None:
        """
        Performs pre-login steps specific to the German VFS website.

        This method checks for a "Reject All" button for cookie policies and
        clicks it if found.

        Args:
            page (playwright.sync_api.Page): The Playwright page object used for browser interaction.
        """
        policies_reject_button = page.get_by_role("button", name="Reject All")
        if policies_reject_button is not None:
            policies_reject_button.click()
            logging.debug("Rejected all cookie policies")

    def check_for_appontment(
        self, page: Page, appointment_params: Dict[str, str]
    ) -> Optional[List[str]]:
        """
        Checks for appointments on the German VFS website based on provided parameters.

        This method clicks the "Start New Booking" button, selects the specified
        visa center, category, and subcategory based on the `appointment_params`
        dictionary. It then extracts the available appointment dates from the
        website and returns them as a list. If no appointments are found, it
        returns None.

        Args:
            page (playwright.sync_api.Page): The Playwright page object used for browser interaction.
            appointment_params (Dict[str, str]): A dictionary containing appointment search criteria.

        Returns:
            Optional[List[str]]: A list of available appointment dates (empty list if none found),
                including a timestamp of the check, or None if no appointments found.
        """
        page.get_by_role("button", name="Start New Booking").click()

        # Select Visa Centre

        visa_centre_dropdown = page.wait_for_selector("mat-form-field")
        visa_centre_dropdown.click()
        visa_centre_dropdown_option = page.wait_for_selector(
            f'mat-option:has-text("{appointment_params.get("visa_center")}")'
        )
        visa_centre_dropdown_option.click()

        # Select Visa Category
        visa_category_dropdown = page.query_selector_all("mat-form-field")[1]
        visa_category_dropdown.click()
        visa_category_dropdown_option = page.wait_for_selector(
            f'mat-option:has-text("{appointment_params.get("visa_category")}")'
        )
        visa_category_dropdown_option.click()

        # Select Subcategory
        visa_subcategory_dropdown = page.query_selector_all("mat-form-field")[2]
        visa_subcategory_dropdown.click()
        visa_subcategory_dropdown_option = page.wait_for_selector(
            f'mat-option:has-text("{appointment_params.get("visa_sub_category")}")'
        )
        visa_subcategory_dropdown_option.click()

        try:
            page.wait_for_selector("div.alert")
            appointment_date_elements = page.query_selector_all("div.alert")
            appointment_dates = []
            for appointment_date_element in appointment_date_elements:
                appointment_date_text = appointment_date_element.text_content()
                appointment_date = extract_date_from_string(appointment_date_text)
                if appointment_date is not None and len(appointment_date) > 0:
                    appointment_dates.append(appointment_date)
            return appointment_dates
        except Exception:
            return None

        return None
