class AppConfig:
    def __init__(self, config_dict, **kwargs):
        self._features_directory = config_dict['features.directory'] = kwargs['features_directory']
        self.output_directory = config_dict['output.directory'] = kwargs['output_directory']
        self._download_feature_files = config_dict.get('download.feature.files', False)
        self._log_file = config_dict.get('log.file', None)
        self._logging_level = config_dict.get('logging.level', 'info')
        self._proj_mgmt_authenticator = config_dict.get('project.management.authenticator', 'keyring')
        self._proj_mgmt_class = config_dict.get('project.management', 'jira')
        self._test_class = config_dict.get('test.class', 'Behave')
        self._use_local_feature_files = config_dict.get('use.local.feature.files', True)
        self.runtime_features_directory = self._features_directory
        self._upload_test_results = config_dict.get('upload.test.results', False)

        self._config_dict = config_dict.copy()

    @property
    def config_dict(self):
        return self._config_dict.copy()

    @property
    def features_directory(self):
        return self._features_directory
    
    @property
    def download_feature_files(self):
        return self._download_feature_files
    
    @property
    def log_file(self):
        return self._log_file

    @property
    def logging_level(self):
        return self._logging_level

    @property
    def proj_mgmt_authenticator(self):
        return self._proj_mgmt_authenticator

    @property
    def proj_mgmt_class(self):
        return self._proj_mgmt_class

    @property
    def test_class(self):
        return self._test_class
    
    @property
    def use_local_feature_files(self):
        return self._use_local_feature_files
