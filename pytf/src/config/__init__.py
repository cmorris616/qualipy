import yaml
import os

from .app_config import AppConfig

_runtime_config: AppConfig = None


def get_config():
    return _runtime_config

def load_config(config_file_name, cl_args={}):
    if not os.path.exists(config_file_name):
        print(
            f"\n*** '{config_file_name}' not found.  Using default configuration. ***\n")
        yaml_config = {}
    else:
        with open(config_file_name, 'r') as config_file:
            yaml_config = yaml.safe_load(config_file)
            if yaml_config is None:
                yaml_config = {}

    if cl_args.features_dir is not None:
        features_directory = cl_args.features_dir
    elif 'features_directory' in yaml_config:
        features_directory = yaml_config['features_directory']
    else:
        features_directory = 'features'

    global _runtime_config
    _runtime_config = AppConfig(yaml_config,
        features_directory=features_directory
    )
