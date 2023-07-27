from unittest.mock import Mock, patch

import pytest

@pytest.fixture()
def mock_keyring(monkeypatch):
    def get_username_mock():
        return 'mock username'
    
    with patch('keyring') as keyring_mock:
        yield keyring_mock
