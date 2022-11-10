from .test_plugin import TestPlugin
from config.app_config import AppConfig


class BehavePlugin(TestPlugin):
    def execute(config: AppConfig):
        from behave.__main__ import main as behave_main
        behave_main(config.features_directory)