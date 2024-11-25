from abc import ABC


class IFactory(ABC):
    """
    Abstract base class for messaging services.
    """

    def __init__(self) -> None:
        super().__init__()
        pass


