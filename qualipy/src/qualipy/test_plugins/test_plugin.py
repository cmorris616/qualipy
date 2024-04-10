"""
This module contains the base class for test plugins.
"""
import abc
from qualipy.config import AppConfig


class TestPlugin(abc.ABC):
    """
    This is the base class for test plugins.
    """

    def __init__(self, config: AppConfig):
        """
        Initializes this class with the application configuration.

        :param config: The application configuration
        """
        self._config = config
    
    @abc.abstractmethod
    def execute(self):
        """
        Executes the tests using the associated testing framework.
        """
        raise NotImplementedError()
    
    @property
    @abc.abstractmethod
    def test_results_file(self):
        """
        The file that contains the test results.
        """
        raise NotImplementedError()
