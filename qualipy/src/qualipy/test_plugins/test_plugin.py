import abc
from qualipy.config import AppConfig


class TestPlugin(abc.ABC):

    def __init__(self, config: AppConfig):
        self._config = config
    
    @abc.abstractmethod
    def execute(self):
        raise NotImplementedError()
    
    @abc.abstractproperty
    def test_results_file(self):
        raise NotImplementedError()
