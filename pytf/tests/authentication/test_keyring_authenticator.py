from unittest.mock import patch

from authentication.keyring_authenticator import KeyringAuthenticator


class TestKeyringAuthenticator:

    @patch('authentication.keyring_authenticator.keyring')
    def test_get_username(self, keyring_mock):
        authenticator = KeyringAuthenticator(system='test')
        authenticator.get_username()
        keyring_mock.get_password.assert_called_with('test', 'username')
