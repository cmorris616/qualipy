from unittest.mock import Mock, patch

import pytest
import os

@pytest.fixture(autouse=True, scope='session')
def unittest_config():
    config_file_name = 'unittest_load_config.yaml'

    with open(config_file_name, 'w') as config_file:
        yield
    
    os.remove(config_file_name)

    import shutil
    shutil.rmtree('features')
