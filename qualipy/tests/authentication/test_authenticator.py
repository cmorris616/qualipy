from qualipy.authentication.authenticator import Authenticator
from unittest import TestCase


class TestAuthenticator(TestCase):
    def test_get_username(self):
        authenticator = Authenticator(system='test')
        self.assertRaises(NotImplementedError, authenticator.get_username)

    def test_get_password(self):
        authenticator = Authenticator(system='test')
        self.assertRaises(NotImplementedError, authenticator.get_password)

    def test_get_api_key(self):
        authenticator = Authenticator(system='test')
        self.assertRaises(NotImplementedError, authenticator.get_api_key)

    def test_get_certificate(self):
        authenticator = Authenticator(system='test')
        self.assertRaises(NotImplementedError, authenticator.get_certificate)