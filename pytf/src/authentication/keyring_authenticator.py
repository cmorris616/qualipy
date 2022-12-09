from .authenticator import Authenticator
import keyring

class KeyringAuthenticator(Authenticator):

    def __init__(self, **kwargs):
        self._system = kwargs['system']
    
    def get_username(self):
        return keyring.get_password(self._system, 'username')
    
    def get_password(self):
        return keyring.get_password(self._system, 'password')

    def get_api_key(self):
        return keyring.get_password(self._system, 'api_key')
    
    def get_certificate(self):
        return keyring.get_password(self._system, 'certificate')
