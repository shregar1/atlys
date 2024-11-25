from abstractions.service import IService


class IMessagingService(IService):

    def __init__(self, urn: str = None, api_name: str = None) -> None:
        super().__init__(urn, api_name)
        pass

    def send():
        pass