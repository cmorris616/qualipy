from unittest import TestCase

from pytf.config.app_config import AppConfig


class TestAppConfig(TestCase):
    def test_app_config_init(self):
        config_dict = {}
        self.assertRaises(KeyError, AppConfig, config_dict)

        features_directory = '/path/to/features'
        self.assertRaises(KeyError, AppConfig, config_dict,
                          features_directory=features_directory)

        output_directory = '/path/to/output'
        config = AppConfig(config_dict,
                          features_directory=features_directory,
                          output_directory=output_directory)

        self.assertEqual(config_dict['features.directory'], config.runtime_features_directory)
        self.assertEqual(config_dict['output.directory'], config.output_directory)

    def test_config_dict(self):
        config_dict = {}

        features_directory = '/path/to/features'
        output_directory = '/path/to/output'

        config = AppConfig(config_dict,
                          features_directory=features_directory,
                          output_directory=output_directory)
        
        self.assertEqual(config_dict, config.config_dict)
        
        config_dict['features.directory'] = 'new directory'
        self.assertNotEqual(config_dict, config.config_dict)
        
        config_dict['features.directory'] = features_directory
        self.assertEqual(config_dict, config.config_dict)
        
        config_dict['output.directory'] = 'new directory'
        self.assertNotEqual(config_dict, config.config_dict)
        
        config_dict['output.directory'] = output_directory
        self.assertEqual(config_dict, config.config_dict)
        
    def test_features_directory(self):
        config_dict = {}

        features_directory = '/path/to/features'
        output_directory = '/path/to/output'

        config = AppConfig(config_dict,
                          features_directory=features_directory,
                          output_directory=output_directory)
        
        self.assertEqual(config.features_directory, features_directory)
        self.assertEqual(config.runtime_features_directory, features_directory)
        
    def test_output_directory(self):
        config_dict = {}

        features_directory = '/path/to/features'
        output_directory = '/path/to/output'

        config = AppConfig(config_dict,
                          features_directory=features_directory,
                          output_directory=output_directory)
        
        self.assertEqual(config.output_directory, output_directory)
        
    def test_download_feature_files(self):
        config_dict = {}

        features_directory = '/path/to/features'
        output_directory = '/path/to/output'

        config = AppConfig(config_dict,
                          features_directory=features_directory,
                          output_directory=output_directory)
        
        self.assertFalse(config.download_feature_files)

        config_dict['download.feature.files'] = False
        config = AppConfig(config_dict,
                          features_directory=features_directory,
                          output_directory=output_directory)
        
        self.assertFalse(config.download_feature_files)

        config_dict['download.feature.files'] = True
        config = AppConfig(config_dict,
                          features_directory=features_directory,
                          output_directory=output_directory)
        
        self.assertTrue(config.download_feature_files)
        
    def test_log_file(self):
        config_dict = {}

        features_directory = '/path/to/features'
        output_directory = '/path/to/output'
        log_file = '/path/to/log/file'

        config = AppConfig(config_dict,
                          features_directory=features_directory,
                          output_directory=output_directory)
        
        self.assertEqual(config.log_file, None)

        config_dict['log.file'] = log_file
        config = AppConfig(config_dict,
                          features_directory=features_directory,
                          output_directory=output_directory)
        
        self.assertEqual(config.log_file, log_file)
        
    def test_logging_level(self):
        config_dict = {}

        features_directory = '/path/to/features'
        output_directory = '/path/to/output'
        logging_level = 'test logging level'

        config = AppConfig(config_dict,
                          features_directory=features_directory,
                          output_directory=output_directory)
        
        self.assertEqual(config.logging_level, 'info')

        config_dict['logging.level'] = logging_level
        config = AppConfig(config_dict,
                          features_directory=features_directory,
                          output_directory=output_directory)
        
        self.assertEqual(config.logging_level, logging_level)
        
    def test_proj_mgmt_authenticator(self):
        config_dict = {}

        features_directory = '/path/to/features'
        output_directory = '/path/to/output'
        authenticator = 'test authenticator'

        config = AppConfig(config_dict,
                          features_directory=features_directory,
                          output_directory=output_directory)
        
        self.assertEqual(config.proj_mgmt_authenticator, 'keyring')

        config_dict['project.management.authenticator'] = authenticator
        config = AppConfig(config_dict,
                          features_directory=features_directory,
                          output_directory=output_directory)
        
        self.assertEqual(config.proj_mgmt_authenticator, authenticator)
        
    def test_proj_mgmt_class(self):
        config_dict = {}

        features_directory = '/path/to/features'
        output_directory = '/path/to/output'
        proj_mgmt_class = 'test proj mgmt class'

        config = AppConfig(config_dict,
                          features_directory=features_directory,
                          output_directory=output_directory)
        
        self.assertEqual(config.proj_mgmt_class, 'jira')

        config_dict['project.management'] = proj_mgmt_class
        config = AppConfig(config_dict,
                          features_directory=features_directory,
                          output_directory=output_directory)
        
        self.assertEqual(config.proj_mgmt_class, proj_mgmt_class)
        
    def test_test_class(self):
        config_dict = {}

        features_directory = '/path/to/features'
        output_directory = '/path/to/output'
        test_class = 'test class'

        config = AppConfig(config_dict,
                          features_directory=features_directory,
                          output_directory=output_directory)
        
        self.assertEqual(config.test_class, 'Behave')

        config_dict['test.class'] = test_class
        config = AppConfig(config_dict,
                          features_directory=features_directory,
                          output_directory=output_directory)
        
        self.assertEqual(config.test_class, test_class)
        
    def test_use_local_feature_files(self):
        config_dict = {}

        features_directory = '/path/to/features'
        output_directory = '/path/to/output'

        config = AppConfig(config_dict,
                          features_directory=features_directory,
                          output_directory=output_directory)
        
        self.assertTrue(config.use_local_feature_files)

        config_dict['use.local.feature.files'] = True
        config = AppConfig(config_dict,
                          features_directory=features_directory,
                          output_directory=output_directory)
        
        self.assertTrue(config.use_local_feature_files)

        config_dict['use.local.feature.files'] = False
        config = AppConfig(config_dict,
                          features_directory=features_directory,
                          output_directory=output_directory)
        
        self.assertFalse(config.download_feature_files)