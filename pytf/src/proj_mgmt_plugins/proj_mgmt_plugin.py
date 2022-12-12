import abc

TESTING_TYPE_REGRESSION = 'regression'
TESTING_TYPE_PROGRESSION = 'progression'


class ProjMgmtPlugin:
    def __init__(self, **kwargs):
        self._authenticator = kwargs.get('authenticator', None)
        self._config = kwargs.get('config', {})
        self._testing_type = self._config.get(
            'testing.type', TESTING_TYPE_REGRESSION)
        self._use_access_token = self._config.get('use.access.token', True)
        self._upload_test_results = self._config.get('upload.test.results', True)

    @abc.abstractmethod
    def export_feature_files(self):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def upload_test_results(self, test_results_file):
        raise NotImplementedError()
