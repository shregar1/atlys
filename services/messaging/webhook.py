import requests

from services.messaging.base import IMessagingService


class WebhookService(IMessagingService):
    """
    Service for sending webhook messages.
    """

    def __init__(self, url):
        self.url = url

    def send(self, data):
        response = requests.post(self.url, json=data)
        return response