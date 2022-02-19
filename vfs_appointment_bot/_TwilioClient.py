import logging

from twilio.rest import Client
from _ConfigReader import _ConfigReader

class _TwilioClient:

    def __init__(self):
        _config_reader = _ConfigReader()
        _section_header = "TWILIO"
        self.to_num = _config_reader.read_prop(_section_header, "twilio_to_num")
        self.from_num = _config_reader.read_prop(_section_header, "twilio_from_num")
        self.account_sid = _config_reader.read_prop(_section_header,"twilio_account_sid")
        self.auth_token = _config_reader.read_prop(_section_header, "twilio_auth_token")
        self.url = _config_reader.read_prop(_section_header,"twilio_url")
        self.sms_enabled = _config_reader.read_bool_prop(_section_header, "twilio_sms_enabled")
        self.call_enabled = _config_reader.read_bool_prop(_section_header, "twilio_call_enabled")

    def send_message(self, message):
        if(not self.sms_enabled):
            logging.debug("SMS is not enabled")
            return

        logging.debug("Sending message")
        try:
            client = Client(self.account_sid, self.auth_token)
            client.messages.create(to=self.to_num, from_=self.from_num, body=message)
            logging.debug("Message sent")
        except Exception as e:
            print("Some problem occured in sending message: {}".format(e))


    def call(self):
        if(not self.call_enabled):
            logging.debug("Call is not enabled")
            return

        logging.debug("Calling")
        try:
            client = Client(self.account_sid, self.auth_token)
            call = client.calls.create(from_=self.from_num, to=self.to_num, url=self.url)
            logging.debug("Call initiated")
        except Exception as e:
            print("Some problem occured in calling: {}".format(e))
