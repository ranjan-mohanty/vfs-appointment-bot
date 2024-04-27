import logging
from typing import Optional

from twilio.rest import Client

from vfs_appointment_bot.notification.notification_client import NotificationClient


class TwilioClient(NotificationClient):
    """Concrete implementation of NotificationClient for the Twilio channel.

    This class provides functionality for sending notifications through the Twilio
    communication platform. It inherits from the abstract `NotificationClient` class
    and implements the required `send_notification` method for Twilio-specific
    notification sending logic, including SMS messages and calls (if enabled).
    """

    def __init__(self):
        """
        Initializes the Twilio client with configuration data.

        This constructor retrieves configuration settings from the "twilio"
        section of the application configuration and validates them using the
        base class validation logic.
        """
        required_config_keys = [
            "to_num",
            "from_num",
            "account_sid",
            "auth_token",
            "url",
            "call_enabled",
        ]
        super().__init__("twilio", required_config_keys)

    def send_notification(self, message: str) -> None:
        """
        Sends a notification message through the Twilio channel.

        This method sends an SMS message using the provided message content.
        Optionally, if the "call_enabled" flag is set to True in the
        configuration, it also initiates a call to the specified phone number
        using a pre-recorded URL (provided by the "url" configuration option).

        Args:
            message (str): The message content to be sent as a Twilio SMS.
        """
        url: Optional[str] = self.config.get("url")
        auth_token: str = self.config.get("auth_token")
        account_sid: str = self.config.get("account_sid")
        to_num: str = self.config.get("to_num")
        from_num: str = self.config.get("from_num")
        call_enabled: bool = self.config.get("call_enabled", False)

        self.__send_message(message, auth_token, account_sid, to_num, from_num)

        if call_enabled:
            self.__call(url, auth_token, account_sid, to_num, from_num)

    def __send_message(
        self,
        message: str,
        auth_token: str,
        account_sid: str,
        to_num: str,
        from_num: str,
    ) -> None:
        """
        Sends an SMS message using the Twilio API.

        This private helper method creates a Twilio client instance and uses it
        to send an SMS message with the provided content to the specified recipient
        phone number.

        Args:
            message (str): The message content to be sent.
            auth_token (str): The Twilio account authentication token.
            account_sid (str): The Twilio account SID.
            to_num (str): The recipient phone number.
            from_num (str): The Twilio phone number used to send the message.
        """
        client = Client(account_sid, auth_token)
        client.messages.create(to=to_num, from_=from_num, body=message)
        logging.info("Message sent successfully!")

    def __call(
        self,
        url: Optional[str],
        auth_token: str,
        account_sid: str,
        to_num: str,
        from_num: str,
    ) -> None:
        """
        Initiates a call using the Twilio API (if URL is provided).

        This private helper method creates a Twilio client instance and uses it
        to initiate a call to the specified recipient phone number, using a
        pre-recorded URL for the call content (if provided in the configuration).

        Args:
            url (Optional[str]): The URL for the pre-recorded call content.
            auth_token (str): The Twilio account authentication token.
            account_sid (str): The Twilio account SID.
            to_num (str): The recipient phone number.
            from_num (str): The Twilio phone number used to initiate the call.
        """
        if url:
            client = Client(account_sid, auth_token)
            client.calls.create(from_=from_num, to=to_num, url=url)
            logging.info("Call request sent successfully!")
        else:
            logging.warning("No URL provided for call request!")
