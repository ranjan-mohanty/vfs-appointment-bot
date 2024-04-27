import smtplib
import logging

from vfs_appointment_bot.notification.notification_client import NotificationClient


class EmailClient(NotificationClient):
    def __init__(self):
        """
        Initializes the email client with configuration data.

        This constructor retrieves configuration settings from the designated
        section (e.g., `"email"`) of the application configuration and
        validates them using the base class validation logic.
        """
        required_keys = ["email", "password"]
        super().__init__("email", required_keys)

    def send_notification(self, message: str) -> None:
        """
        Sends a notification message through the email channel.

        This method sends an email notification using the provided message content.
        It connects securely to the configured SMTP server (e.g., Gmail's SMTP),
        authenticates with the provided credentials, and constructs a well-formatted
        email before sending it.

        Args:
            message (str): The message content to be included in the email.
        """
        email: str = self.config.get("email")
        password: str = self.config.get("password")
        email_text = self.__construct_email_text(email, message)

        smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        smtp_server.ehlo()
        smtp_server.login(email, password)
        smtp_server.sendmail(email, email, email_text)
        smtp_server.close()
        logging.info("Email sent successfully!")

    def __construct_email_text(self, email: str, message: str) -> str:
        """
        Constructs a formatted email text with sender, receiver, subject,
        and message body.

        Args:
            message (str): The message content to be included in the email body.

        Returns:
            str: The formatted email text ready for sending.
        """
        return f"From: {email}\nTo: {email}\nSubject: VFS Appointment Bot Notification\n\n{message}"
