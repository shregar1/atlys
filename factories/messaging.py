from abstractions.factory import IFactory

from services.messaging.email import EmailService
from services.messaging.sms import SMSService
from services.messaging.webhook import WebhookService


class MessagingFactory(IFactory):
    """
    Factory for creating messaging service instances.
    """

    @staticmethod
    def create_service(service_type, **kwargs):
        if service_type == "webhook":
            return WebhookService(kwargs['url'])
        elif service_type == "email":
            return EmailService(kwargs['smtp_server'], kwargs['port'], kwargs['username'], kwargs['password'])
        elif service_type == "sms":
            return SMSService(kwargs['api_url'], kwargs['api_key'])
        else:
            raise ValueError(f"Unknown service type: {service_type}")
