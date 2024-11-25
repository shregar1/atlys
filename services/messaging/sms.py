import requests

from services.messaging.base import IMessagingService


class SMSService(IMessagingService):
    """
    Service for sending SMS messages (e.g., Twilio).
    """

    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def send(self, data):
        """
        Data should include: to, message
        """
        payload = {
            "to": data['to'],
            "message": data['message'],
            "api_key": self.api_key
        }
        response = requests.post(self.api_url, json=payload)
        return response.status_code, response.json()

