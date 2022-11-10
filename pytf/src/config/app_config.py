class AppConfig:
    def __init__(self, **kwargs):
        self._features_directory = kwargs['features_directory']
        self._test_class = kwargs['test_class']
        pass

    @property
    def features_directory(self):
        return self._features_directory
    
    @property
    def test_class(self):
        return self._test_class
