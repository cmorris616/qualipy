from unittest import TestCase
from unittest.mock import Mock
import os

class TestInit(TestCase):
    def test_load_config_no_file(self):
        from qualipy import config
        
        config_file = '/non/existent/file'
        features_directory = '/path/to/features'
        output_directory = '/path/to/output'

        config.load_config(config_file)
        test_config = config.get_config()

        self.assertIsNotNone(test_config)
        self.assertEqual(test_config.features_directory, 'features')
        self.assertEqual(test_config.output_directory, 'qualipy_output')

        clargs = Mock()
        clargs.features_dir = features_directory
        clargs.output_dir = output_directory

        config.load_config(config_file, cl_args=clargs)
        test_config = config.get_config()
        self.assertEqual(test_config.features_directory, features_directory)
        self.assertEqual(test_config.output_directory, output_directory)

    def test_load_config(self):
        from qualipy import config

        features_directory = '/path/to/features'
        output_directory = '/path/to/output'

        config_file_name = 'unittest_load_config.yaml'
        clargs = Mock()

        with open(config_file_name, 'w') as config_file:
            pass

        config.load_config(config_file_name)
        test_config = config.get_config()

        self.assertEqual(test_config.runtime_features_directory, 'features')
        self.assertEqual(test_config.output_directory, 'qualipy_output')

        with open(config_file_name, 'w') as config_file:
            config_file.write(f'''
                              features.directory: {features_directory}
                              output.directory: {output_directory}
                              ''');

        config.load_config(config_file_name)
        test_config = config.get_config()

        self.assertEqual(test_config.runtime_features_directory, features_directory)
        self.assertEqual(test_config.output_directory, output_directory)