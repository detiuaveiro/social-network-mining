from abc import ABC
from abc import abstractmethod


class Bot(ABC):
    __slots__ = ()

    @abstractmethod
    def run(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def user_agent(self):
        """
        User Agent to use when making API calls
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def raw_api(self):
        """
        API of the bot
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def proxy(self):
        raise NotImplementedError

    @abstractmethod
    def start(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def connect_to_api(self):
        raise NotImplementedError

    @abstractmethod
    def close(self):
        """
        Closing connections
        """
        raise NotImplementedError
