from .authenticator import Authenticator

class KeyringAuthenticator(Authenticator):
    
    def get_username(self):
        raise NotImplementedError()
    
    def get_password(self):
        raise NotImplementedError()

    def get_api_key(self):
        raise NotImplementedError()
    
    def get_certificate(self):
        raise NotImplementedError()