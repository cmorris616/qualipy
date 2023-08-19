import os
from .test_plugin import TestPlugin
from qualipy.config.app_config import AppConfig


class BehavePlugin(TestPlugin):
    def __init__(self, config: AppConfig):
        super().__init__(config)
        self._output_file = os.path.join(self._config.output_directory, 'behave_report.json')

    def execute(self):
        from behave.__main__ import main as behave_main
        behave_main([self._config.runtime_features_directory, '-f',
                    'json.pretty', '-o', self._output_file])

    @property
    def test_results_file(self):
        return self._output_file
