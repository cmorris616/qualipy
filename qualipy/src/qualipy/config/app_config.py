"""
This module contains the AppConfig class for retaining the application
configuration during runtime.  This class exposes properties for settings.
In the event that a setting is needed, but is not exposed as a property, this
class can return the entire configuration as a dict via the config_dict
property.  This allows for the addition of custom configuration settings
without the need to modify the code in this class.
"""
class AppConfig:
    """
    This class exposes properties for settings.  In the event that a setting
    is needed, but is not exposed as a property, this class can return the
    entire configuration as a dict via the config_dict property.  This allows
    for the addition of custom configuration settings without the need to
    modify the code in this class.
    """
    def __init__(self, config_dict, **kwargs):
        """
        Initializes this class from the provided config_dict and kwargs.
        """
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
        self._success_story_status = config_dict.get('success.story.status', 'Done')
        self._failed_story_status = config_dict.get('failed.story.status', 'In Progress')

        self._config_dict = config_dict.copy()

    @property
    def config_dict(self):
        """
        The application configuration as a dict.  This will include
        configuration settings that are not coded into this class.
        """
        return self._config_dict.copy()
    
    @property
    def failed_story_status(self):
        """
        The status to which a user story should be moved in the event
        that an associated test has failed.
        """
        return self._failed_story_status

    @property
    def features_directory(self):
        """
        The directory where the feature files are stored.
        """
        return self._features_directory
    
    @property
    def download_feature_files(self):
        """
        Indicates whether or not feature files should be downloaded from
        the project management system.
        """
        return self._download_feature_files
    
    @property
    def log_file(self):
        """
        The location of the log file.
        """
        return self._log_file

    @property
    def logging_level(self):
        """
        The level of logs to be output.  These logging levels are available
        in the Python logging module.
        """
        return self._logging_level
    
    @property
    def move_user_stories(self):
        """
        Indicates whether or not user stories should be moved upon test
        completion.
        """
        return self._move_user_stories

    @property
    def proj_mgmt_authenticator_class(self):
        """
        The fully qualified class name for the authenticator to use for
        interacting with the project management system.
        """
        return self._proj_mgmt_authenticator_class

    @property
    def proj_mgmt_class(self):
        """
        The system name to be used by the authenticator when retrieving
        credentials.
        """
        return self._proj_mgmt_class
    
    @property
    def proj_mgmt_plugin_class(self):
        """
        The fully qualified class name for the project management plugin.
        """
        return self._proj_mgmt_plugin_class
    
    @property
    def success_story_status(self):
        """
        The status to which user stories should be moved upon successful
        completion of all associated tests.
        """
        return self._success_story_status

    @property
    def test_plugin(self):
        """
        The fully qualified class name for the plugin to be used for test
        execution
        """
        return self._test_plugin
    
    @property
    def upload_test_results(self):
        """
        Indicates whether or not to upload test results.
        """
        return self._upload_test_results
    
    @property
    def use_local_feature_files(self):
        """
        Indicates whether or not to use local feature files (i.e. files
        not downloaded from the project management system).
        """
        return self._use_local_feature_files
