class AppConfig:
    def __init__(self, config_dict, **kwargs):
        self._features_directory = config_dict['features.directory'] = kwargs['features_directory']
        self.output_directory = config_dict['output.directory'] = kwargs['output_directory']
        self._download_feature_files = config_dict.get('download.feature.files', False)
        self._move_user_stories = config_dict.get('move.user.stories', False)
        self._log_file = config_dict.get('log.file', None)
        self._logging_level = config_dict.get('logging.level', 'info')
        self._proj_mgmt_authenticator_class = config_dict.get('project.management.authenticator.class', 
                                                              'qualipy.authentication.keyring_authenticator.KeyringAuthenticator')
        self._proj_mgmt_class = config_dict.get('project.management', 'project.management')
        self._proj_mgmt_plugin_class = config_dict.get('project.management.plugin', 
                                                       'qualipy.proj_mgmt_plugins.jira_proj_mgmt_plugin.JiraProjMgmtPlugin')
        self._test_plugin = config_dict.get('test.plugin', 'qualipy.test_plugins.behave_plugin.BehavePlugin')
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
    def move_user_stories(self):
        return self._move_user_stories

    @property
    def proj_mgmt_authenticator_class(self):
        return self._proj_mgmt_authenticator_class

    @property
    def proj_mgmt_class(self):
        return self._proj_mgmt_class
    
    @property
    def proj_mgmt_plugin_class(self):
        return self._proj_mgmt_plugin_class

    @property
    def test_plugin(self):
        return self._test_plugin
    
    @property
    def upload_test_results(self):
        return self._upload_test_results
    
    @property
    def use_local_feature_files(self):
        return self._use_local_feature_files
