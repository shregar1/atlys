import smtplib

from services.messaging.base import IMessagingService


class EmailService(IMessagingService):
    """
    Service for sending email messages.
    """

    def __init__(self, smtp_server, port, username, password):
        self.smtp_server = smtp_server
        self.port = port
        self.username = username
        self.password = password

    def send(self, data):
        """
        Data should include: to, subject, body
        """
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.starttls()
            server.login(self.username, self.password)
            to_email = data['to']
            subject = data['subject']
            body = data['body']
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(self.username, to_email, message)
        return "Email sent successfully"

