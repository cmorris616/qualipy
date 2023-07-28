from unittest.mock import patch

from pytf.authentication.keyring_authenticator import KeyringAuthenticator


class TestKeyringAuthenticator:

    @patch('pytf.authentication.keyring_authenticator.keyring')
    def test_get_username(self, keyring_mock):
        authenticator = KeyringAuthenticator(system='test')
        authenticator.get_username()
        keyring_mock.get_password.assert_called_with('test', 'username')

    @patch('pytf.authentication.keyring_authenticator.keyring')
    def test_get_password(self, keyring_mock):
        authenticator = KeyringAuthenticator(system='test')
        authenticator.get_password()
        keyring_mock.get_password.assert_called_with('test', 'password')

    @patch('pytf.authentication.keyring_authenticator.keyring')
    def test_get_api_key(self, keyring_mock):
        authenticator = KeyringAuthenticator(system='test')
        authenticator.get_api_key()
        keyring_mock.get_password.assert_called_with('test', 'api_key')

    @patch('pytf.authentication.keyring_authenticator.keyring')
    def test_get_certificate(self, keyring_mock):
        authenticator = KeyringAuthenticator(system='test')
        authenticator.get_certificate()
        keyring_mock.get_password.assert_called_with('test', 'certificate')
