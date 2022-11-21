import abc


class Authenticator:
    def __init__(self, config):
        self._config = config
    
    @abc.abstractmethod
    def get_username(self):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def get_password(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_api_key(self):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def get_certificate(self):
        raise NotImplementedError()
