import abc

TESTING_TYPE_REGRESSION = 'regression'
TESTING_TYPE_PROGRESSION = 'progression'

class ProjMgmtPlugin:
    def __init__(self, **kwargs):
        self._authenticator = kwargs.get('authenticator', None)
        self._config = kwargs.get('config', {})
        self._testing_type = kwargs.get('testing_type', TESTING_TYPE_REGRESSION)
    
    @abc.abstractmethod
    def export_feature_files(self):
        raise NotImplementedError()
