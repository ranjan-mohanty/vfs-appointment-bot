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
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class _VfsClient:

    def __init__(self):
        self._twilio_client = _TwilioClient()
        self._telegram_client = _TelegramClient()
        self._config_reader = _ConfigReader()

        self._use_telegram = self._config_reader.read_prop("DEFAULT", "use_telegram")
        self._use_twilio = self._config_reader.read_prop("DEFAULT", "use_twilio")
        logging.info("Will use Telegram : {}".format(self._use_telegram))
        logging.info("Will use Twilio : {}".format(self._use_twilio))

        self._init_web_driver()

    def _init_web_driver(self):
        logging.info("Initialising the browser")
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
        logging.info("Browser initialised")

    def _login(self):

        _section_header = "VFS"
        _email = self._config_reader.read_prop(_section_header, "vfs_email");
        _password = self._config_reader.read_prop(_section_header, "vfs_password");

        logging.info("Loading the login page")
        # logging in
        time.sleep(30)
        logging.info("Logging in with email: {}".format(_email))

        try:
            # sleep provides sufficient time for all the elements to get visible
            logging.info("Choosing email input")
            _email_input = self._web_driver.find_element(By.ID, "mat-input-0")
            _email_input.send_keys(_email)
            logging.info("Choosing password input")
            _password_input = self._web_driver.find_element(By.ID, "mat-input-1")
            _password_input.send_keys(_password)
            logging.info("Choosing login button")
            _login_button = self._web_driver.find_element(By.XPATH, '//button/span[1]')
            _login_button.click()
        except Exception as e:
            logging.info("Couldn't fill out login form")
            logging.info(e.args[0])
            #logging.info(self._web_driver.page_source)
            if "You do not have access" in self._web_driver.page_source:
                logging.info("Request is banned by CloudFlare")
            raise e

        logging.info("Requested login, waiting to log in")
        time.sleep(30)

    def _validate_login(self):
        try:
#            _new_booking_button = self._web_driver.find_element_by_xpath("//section/div/div[2]/button/span")
            _new_booking_button = self._web_driver.find_element(By.XPATH, '/html/body/app-root/div/app-dashboard/section[1]/div/div[2]/button/span[1]')
            if _new_booking_button == None:
                logging.info("Unable to login. VFS website is not responding")
                #logging.info(self._web_driver.page_source)
                raise Exception("Unable to login. VFS website is not responding")
            else:
                logging.info("Logged in successfully")
        except:
            logging.info("Unable to login. VFS website is not responding")
            #logging.info(self._web_driver.page_source)
            raise Exception("Unable to login. VFS website is not responding")

        time.sleep(5)
        _new_booking_button = self._web_driver.find_element(By.XPATH,
            "//section/div/div[2]/button/span"
        )
        _new_booking_button.click()


    def _get_appointment_date(self, centre_param):
        visa_centre = centre_param[0]
        category = centre_param[1]
        sub_category = centre_param[2]

        logging.info("Getting appointment date: Visa Centre: {}, Category: {}, Sub-Category: {}".format(visa_centre, category, sub_category))

        time.sleep(5)
        #logging.info("Choosing visa centre")
        _visa_centre_dropdown = self._web_driver.find_element(By.XPATH,
            "//mat-form-field/div/div/div[3]"
        )
        _visa_centre_dropdown.click()
        time.sleep(5)

        #logging.info("Trying to choose visa centre")
        try:
            _visa_centre = self._web_driver.find_element(By.XPATH,
                "//mat-option[starts-with(@id,'mat-option-')]/span[contains(text(), '{}')]".format(visa_centre)
            )
        except NoSuchElementException:
            raise Exception("Visa centre not found: {}".format(visa_centre))

        logging.info("VFS Centre: " + _visa_centre.text)
        self._web_driver.execute_script("arguments[0].click();", _visa_centre)
        time.sleep(5)

        #logging.info("Choosing category")
        _category_dropdown = self._web_driver.find_element(By.XPATH,
            "//div[@id='mat-select-value-3']"
        )
        _category_dropdown.click()
        time.sleep(5)

        try:
            _category = self._web_driver.find_element(By.XPATH,
                "//mat-option[starts-with(@id,'mat-option-')]/span[contains(text(), '{}')]".format(category)
            )
        except NoSuchElementException:
            raise Exception("Category not found: {}".format(category))

        logging.info("Category: " + _category.text)
        self._web_driver.execute_script("arguments[0].click();", _category)
        time.sleep(5)

        _subcategory_dropdown = self._web_driver.find_element(By.XPATH,
            "//div[@id='mat-select-value-5']"
        )

        self._web_driver.execute_script("arguments[0].click();", _subcategory_dropdown)
        time.sleep(5)

        try:
            _subcategory = self._web_driver.find_element(By.XPATH,
                "//mat-option[starts-with(@id,'mat-option-')]/span[contains(text(), '{}')]".format(sub_category)
            )
        except NoSuchElementException:
            raise Exception("Sub-category not found: {}".format(sub_category))

        self._web_driver.execute_script("arguments[0].click();", _subcategory)
        logging.info("Sub-Cat: " + _subcategory.text)
        #logging.info("Awaiting response")
        time.sleep(10)

        # read contents of the text box
        contents = self._web_driver.find_element(By.XPATH,"//div[4]/div")
        logging.info("Found response")
        return contents

    def check_slot(self, country, vfs_url, centre_params):

        # open the webpage
        self.vfs_login_url = vfs_url
        self._web_driver.delete_all_cookies()
        self._web_driver.get(self.vfs_login_url)

        self._login()
        self._validate_login()

        for centre_param in centre_params:
            logging.info("Checking for params: {}".format(centre_param))

            _message = self._get_appointment_date(centre_param)
            logging.info("Message: " + _message.text)

            if len(_message.text) != 0 and "No appointment slots" not in _message.text:
                for i in range(5):
                    logging.info("======================================================")
                logging.info("Appointment slots available: {}".format(_message.text))
                ts = time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
                message = "{}: {}, {}, msg: {}".format(st, country, centre_param[2], _message.text)
                if eval(self._use_telegram):
                    self._telegram_client.send_message(message)
                if eval(self._use_twilio):
                    self._twilio_client.send_message(message)
                    self._twilio_client.call()
            else:
                logging.info("No slots available")

        # Otherwise some inactivity issues happen sometimes.
        self._web_driver.get("https://google.com")


    def close(self):
        self._web_driver.quit()
