import abc
from config import AppConfig


class TestPlugin(abc.ABC):

    def __init__(self, config: AppConfig):
        self._config = config
    
    @abc.abstractmethod
    def execute(self):
        raise NotImplementedError()
