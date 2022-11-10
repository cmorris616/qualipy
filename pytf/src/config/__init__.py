import yaml
import os
import logging

from .app_config import AppConfig

_runtime_config: AppConfig = None


def get_config():
    return _runtime_config

def load_config(config_file, cl_args={}):
    if os.path.exists(config_file):
        logging.info(
            f"'{config_file}' not found.  Using default configuration.")
        yaml_config = {}
    else:
        yaml_config = yaml.safe_load(config_file)

    if cl_args.features_dir is not None:
        features_directory = cl_args.features_directory
    elif 'features_directory' in yaml_config:
        features_directory = yaml_config['features_directory']
    else:
        features_directory = 'features'

    global _runtime_config
    _runtime_config = AppConfig(
        features_directory=features_directory,
        test_class=yaml_config.get('test_class', 'Behave')
    )
