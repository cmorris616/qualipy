import abc
from config import AppConfig


class TestPlugin(abc.ABC):
    @abc.abstractmethod
    def execute(self, config: AppConfig):
        raise NotImplementedError()
