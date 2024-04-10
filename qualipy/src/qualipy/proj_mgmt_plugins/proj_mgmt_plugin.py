"""
This module contains the base class for the project management plugins.
The project management plugins are used to interact with project
management systems such as JIRA.
"""

import abc

TESTING_TYPE_REGRESSION = 'regression'
TESTING_TYPE_PROGRESSION = 'progression'


class ProjMgmtPlugin:
    """
    This is the base class for the project management plugins.
    """
    def __init__(self, **kwargs):
        """
        Initializes this class based on the values in kwargs.

        :param kwargs: Keyword arguments
            * authenticator: The authenticator to be used when interacting with
                             the project management system.

            * config: The application configuration dict.  This provides the
                      project management plugin with the ability to use custom
                      configuration settings.
        """
        self._authenticator = kwargs.get('authenticator', None)
        self._config = kwargs.get('config', {})
        self._testing_type = self._config.get(
            'testing.type', TESTING_TYPE_REGRESSION)
        self._use_access_token = self._config.get('use.access.token', True)
        self._upload_test_results = self._config.get('upload.test.results', True)

    @abc.abstractmethod
    def export_feature_files(self):
        """
        Exports the feature files from the project management system.
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def move_user_stories(self):
        """
        Moves the user stories after the tests have completed
        (for progression testing only).
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def upload_test_results(self, test_results_file):
        """
        Uploads the test results to the project management system.
        """
        raise NotImplementedError()
