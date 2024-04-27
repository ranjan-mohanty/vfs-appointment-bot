from abc import ABC, abstractmethod
from typing import List

from vfs_appointment_bot.utils.config_reader import get_config_section


class NotificationClient(ABC):
    """Abstract base class for notification clients.

    This class defines the common interface for notification clients used
    throughout the application. Subclasses must implement the `send_notification`
    method to provide specific notification sending functionality for their
    respective channels.
    """

    def __init__(self, config_section: str, required_config_keys: List[str]):
        """
        Initializes the client with configuration data.

        Args:
            config_section (str): The name of the configuration section
                containing client-specific settings.
            required_config_keys (list[str]): A list of required keys that must be
                present in the configuration section.
        """
        self.required_keys = required_config_keys
        self.config = get_config_section(config_section)
        self._validate_config(required_config_keys)

    @abstractmethod
    def send_notification(self, message: str) -> None:
        """
        Sends a notification message to the recipient.

        This method is abstract and must be implemented by subclasses to
        provide the specific logic for sending notifications through their
        respective channels.

        Args:
            message (str): The message content to be sent.
        """

    def _validate_config(self, required_config_keys: list[str]):
        """
        Validates the configuration of the notification client.

        This method checks if all required configuration keys are present
        and have non-null values. If any validation errors are found,
        appropriate exceptions are raised.

        Args:
            required_config_keys (list[str]): A list of required keys that must be
                present in the configuration section.
        """
        missing_keys = required_config_keys - self.config.keys()
        if missing_keys:
            raise NotificationClientConfigValidationError(
                f"Missing required configuration keys: {', '.join(missing_keys)}"
            )

        for key in self.required_keys:
            if self.config.get(key) is None:
                raise NotificationClientConfigValidationError(
                    f"Value for key '{key}' cannot be null."
                )


class NotificationClientConfigValidationError(Exception):
    """Exception raised when notification client configuration validation fails."""


class NotificationClientError(Exception):
    """Exception raised when an error occurs during notification sending."""
