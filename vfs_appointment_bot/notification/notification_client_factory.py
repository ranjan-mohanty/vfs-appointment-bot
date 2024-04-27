from vfs_appointment_bot.notification.notification_client import NotificationClient


class UnsupportedNotificationChannelError(Exception):
    """Raised when an unsupported notification channel is provided."""


def get_notification_client(channel: str) -> NotificationClient:
    """Retrieves the appropriate notification client for a given channel.

    This function creates an instance of a notification client class based on the
    provided channel string. Currently supported channels include "telegram" and
    "slack". If an unsupported channel is provided, a `ValueError` exception is
    raised.

    Args:
        channel (str): The notification channel name.

    Returns:
        NotificationClient: An instance of the `NotificationClient` sub class specific to the provided channel.

    Raises:
        UnsupportedNotificationChannelError: If the provided notification channel is not supported.
    """

    if channel == "telegram":
        from .telegram_client import TelegramClient

        return TelegramClient()
    elif channel == "slack":
        from .twilio_client import TwilioClient

        return TwilioClient()
    elif channel == "email":
        from .email_client import EmailClient

        return EmailClient()
    else:
        raise UnsupportedNotificationChannelError(
            f"Notification channel '{channel}' is not supported"
        )
