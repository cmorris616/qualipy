import abc

class ProjMgmtPlugin:
    def __init__(self, config):
        self._config = config
    
    @abc.abstractmethod
    def export_feature_files(self):
        raise NotImplementedError()
