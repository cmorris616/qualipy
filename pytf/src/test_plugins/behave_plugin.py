from .test_plugin import TestPlugin
from config.app_config import AppConfig


class BehavePlugin(TestPlugin):
    def execute(self):
        from behave.__main__ import main as behave_main
        behave_main(self._config.features_directory)