"""
This module contains the interface that should be extended by authenticator classes.
"""
import abc


class Authenticator:
    """
    This is the interface that should be extended by authenticator classes.
    """
    def __init__(self, **kwargs):
        pass
    
    @abc.abstractmethod
    def get_username(self):
        """
        Returns the username for this authenticator
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def get_password(self):
        """
        Returns the password for this authenticator
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_api_key(self):
        """
        Returns the API key for this authenticator
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def get_certificate(self):
        """
        Returns the certificate for this authenticator
        """
        raise NotImplementedError()
