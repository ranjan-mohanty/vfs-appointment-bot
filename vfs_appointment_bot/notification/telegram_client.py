import logging

import requests

from vfs_appointment_bot.notification.notification_client import NotificationClient


class TelegramClient(NotificationClient):
    """Concrete implementation of NotificationClient for the Telegram channel.

    This class provides functionality for sending notifications through the Telegram
    messaging platform. It inherits from the abstract `NotificationClient` class
    and implements the required `send_notification` method for Telegram-specific
    notification sending logic.
    """

    def __init__(self):
        """
        Initializes the Telegram client with configuration data.

        This constructor retrieves configuration settings from the "telegram"
        section of the application configuration and validates them using the
        base class validation logic.
        """
        required_keys = ["bot_token", "chat_id", "parse_mode"]
        super().__init__("telegram", required_keys)

    def send_notification(self, message: str) -> None:
        """
        Sends a notification message through the Telegram channel.

        This method constructs a Telegram API request URL using the retrieved
        configuration settings (bot token, chat ID, and parse mode) and sends a
        GET request to the Telegram API with the message content. The response
        from the Telegram API is logged for debugging purposes.

        Args:
            message (str): The message content to be sent as a Telegram notification.
        """
        bot_token: str = self.config.get("bot_token")
        chat_id: str = self.config.get("chat_id")
        parse_mode: str = self.config.get("parse_mode")

        url = (
            f"https://api.telegram.org/bot{bot_token}/sendMessage?"
            + f"chat_id={chat_id}&parse_mode={parse_mode}&text={message}"
        )
        requests.get(url, timeout=3000).json()
        logging.info("Telegram message sent successfully!")
