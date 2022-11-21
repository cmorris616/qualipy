class AppConfig:
    def __init__(self, **kwargs):
        self._features_directory = kwargs['features_directory']
        self._log_file = kwargs['log_file']
        self._logging_level = kwargs['logging_level']
        self._proj_mgmt_class = kwargs['proj_mgmt_class']
        self._test_class = kwargs['test_class']

    @property
    def features_directory(self):
        return self._features_directory
    
    @property
    def log_file(self):
        return self._log_file

    @property
    def logging_level(self):
        return self._logging_level

    @property
    def proj_mgmt_class(self):
        return self._proj_mgmt_class
    
    @property
    def test_class(self):
        return self._test_class
