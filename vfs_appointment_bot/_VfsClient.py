from cmath import exp
import email
import time
import logging
import datetime

from _ConfigReader import _ConfigReader
from _TwilioClient import _TwilioClient
from _TelegramClient import _TelegramClient


from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException

class _VfsClient:

    def __init__(self):
        self._twilio_client = _TwilioClient()
        self._telegram_client = _TelegramClient()
        self._config_reader = _ConfigReader()

        self._use_telegram = self._config_reader.read_prop("DEFAULT", "use_telegram")
        self._use_twilio = self._config_reader.read_prop("DEFAULT", "use_twilio")
        logging.debug("Will use Telegram : {}".format(self._use_telegram))
        logging.debug("Will use Twilio : {}".format(self._use_twilio))

    def _init_web_driver(self):
        firefox_options = Options()

        # open in headless mode to run in background
        firefox_options.headless = True
        # firefox_options.add_argument("start-maximized")

        # following options reduce the RAM usage
        firefox_options.add_argument("disable-infobars")
        firefox_options.add_argument("--disable-extensions")
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-application-cache")
        firefox_options.add_argument("--disable-gpu")
        firefox_options.add_argument("--disable-dev-shm-usage")
        self._web_driver = webdriver.Firefox(options=firefox_options)

        # make sure that the browser is full screen,
        # else some buttons will not be visible to selenium
        self._web_driver.maximize_window()

    def _login(self):

        _section_header = "VFS"
        _email = self._config_reader.read_prop(_section_header, "vfs_email");
        _password = self._config_reader.read_prop(_section_header, "vfs_password");

        logging.debug("Logging in with email: {}".format(_email))

        # logging in
        time.sleep(10)

        # sleep provides sufficient time for all the elements to get visible
        _email_input = self._web_driver.find_element_by_xpath("//input[@id='mat-input-0']")
        _email_input.send_keys(_email)
        _password_input = self._web_driver.find_element_by_xpath("//input[@id='mat-input-1']")
        _password_input.send_keys(_password)
        _login_button = self._web_driver.find_element_by_xpath("//button/span")
        _login_button.click()
        time.sleep(10)

    def _validate_login(self):
        try:
            _new_booking_button = self._web_driver.find_element_by_xpath("//section/div/div[2]/button/span")
            if _new_booking_button == None:
                logging.debug("Unable to login. VFS website is not responding")
                raise Exception("Unable to login. VFS website is not responding")
            else:
                logging.debug("Logged in successfully")
        except:
            logging.debug("Unable to login. VFS website is not responding")
            raise Exception("Unable to login. VFS website is not responding")

    def _get_appointment_date(self, visa_centre, category, sub_category):
        logging.info("Getting appointment date: Visa Centre: {}, Category: {}, Sub-Category: {}".format(visa_centre, category, sub_category))
        # select from drop down
        _new_booking_button = self._web_driver.find_element_by_xpath(
            "//section/div/div[2]/button/span"
        )
        _new_booking_button.click()
        time.sleep(5)
        _visa_centre_dropdown = self._web_driver.find_element_by_xpath(
            "//mat-form-field/div/div/div[3]"
        )
        _visa_centre_dropdown.click()
        time.sleep(2)

        try:
            _visa_centre = self._web_driver.find_element_by_xpath(
                "//mat-option[starts-with(@id,'mat-option-')]/span[contains(text(), '{}')]".format(visa_centre)
            )
        except NoSuchElementException:
            raise Exception("Visa centre not found: {}".format(visa_centre))

        logging.debug("VFS Centre: " + _visa_centre.text)
        self._web_driver.execute_script("arguments[0].click();", _visa_centre)
        time.sleep(5)

        _category_dropdown = self._web_driver.find_element_by_xpath(
            "//div[@id='mat-select-value-3']"
        )
        _category_dropdown.click()
        time.sleep(5)

        try:
            _category = self._web_driver.find_element_by_xpath(
                "//mat-option[starts-with(@id,'mat-option-')]/span[contains(text(), '{}')]".format(category)
            )
        except NoSuchElementException:
            raise Exception("Category not found: {}".format(category))

        logging.debug("Category: " + _category.text)
        self._web_driver.execute_script("arguments[0].click();", _category)
        time.sleep(5)

        _subcategory_dropdown = self._web_driver.find_element_by_xpath(
            "//div[@id='mat-select-value-5']"
        )

        self._web_driver.execute_script("arguments[0].click();", _subcategory_dropdown)
        time.sleep(5)

        try:
            _subcategory = self._web_driver.find_element_by_xpath(
                "//mat-option[starts-with(@id,'mat-option-')]/span[contains(text(), '{}')]".format(sub_category)
            )
        except NoSuchElementException:
            raise Exception("Sub-category not found: {}".format(sub_category))

        self._web_driver.execute_script("arguments[0].click();", _subcategory)
        logging.debug("Sub-Cat: " + _subcategory.text)
        time.sleep(5)

        # read contents of the text box
        return self._web_driver.find_element_by_xpath("//div[4]/div")

    def check_slot(self, visa_centre, category, sub_category):
        self._init_web_driver()

        # open the webpage
        self.vfs_login_url = self._config_reader.read_prop("VFS", "vfs_login_url")
        self._web_driver.get(self.vfs_login_url)

        self._login()
        self._validate_login()

        _message = self._get_appointment_date(visa_centre, category, sub_category)
        logging.debug("Message: " + _message.text)

        if len(_message.text) != 0 and _message.text != "No appointment slots are currently available" and _message.text != "Currently No slots are available for selected category, please confirm waitlist\nTerms and Conditions":
            logging.info("Appointment slots available: {}".format(_message.text))
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
            message = "{} at {}".format(_message.text, st)
            if eval(self._use_telegram):
                self._telegram_client.send_message(message)
            if eval(self._use_twilio):
                self._twilio_client.send_message(message)
                self._twilio_client.call()
        else:
            logging.info("No slots available")
        # Close the browser
        self._web_driver.close()
        self._web_driver.quit()
