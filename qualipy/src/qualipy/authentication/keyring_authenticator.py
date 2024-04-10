"""
This module contains the class that handles retrieving credentials
from the OS keyring.
"""
from .authenticator import Authenticator
import keyring

class KeyringAuthenticator(Authenticator):
    """
    This class handles retrieving credentials from the OS keyring.
    The credentials are stored using the service to which the credentials
    pertain and the attribute being stored.

        keyring set [service] [attribute]

    For example, the username for JIRA would be stored in the OS keyring
    with the service being "jira" and the attribute being "username".
    In order to store the username for JIRA, the below command can be used.

        keyring set jira username

    When prompted, type the username to be used for logging into JIRA.

    To store the password for JIRA, the below command could be used.

        keyring set jira password

    When prompted, type the password to be used for logging into JIRA.

    Available attributes to set are:

        * username
        * password
        * api_key
        * certificate
    """
    def __init__(self, **kwargs):
        """
        Initialized this class by setting the system name to be used when
        retrieving credentials from the OS keyring.

        :param kwargs:
            * system: the system name to use when retrieving credentials
              from the OS keyring (i.e. jira).
        """
        self._system = kwargs['system']
    
    def get_username(self):
        return keyring.get_password(self._system, 'username')
    
    def get_password(self):
        return keyring.get_password(self._system, 'password')

    def get_api_key(self):
        return keyring.get_password(self._system, 'api_key')
    
    def get_certificate(self):
        return keyring.get_password(self._system, 'certificate')
