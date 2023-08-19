import argparse
import logging
import os
import shutil

from qualipy.config import get_config, load_config
from qualipy.proj_mgmt_plugins.jira_proj_mgmt_plugin import JiraProjMgmtPlugin
from qualipy.authentication.keyring_authenticator import KeyringAuthenticator
from qualipy.test_plugins.behave_plugin import BehavePlugin

OUTPUT_DIRECTORY = 'qualipy_output'

parser = argparse.ArgumentParser(
    prog='QualiPy - Python Testing Framework',
    description='Adds automation to the testing process'
)

parser.add_argument('--config-file', default='qualipy.yaml')
parser.add_argument('--features-dir')
parser.add_argument('--output-dir', default=OUTPUT_DIRECTORY)

args = parser.parse_args()

load_config(args.config_file, args)
config = get_config()

# Setup logging
logging_levels = {
    'critical': logging.CRITICAL,
    'debug': logging.DEBUG,
    'error': logging.ERROR,
    'fatal': logging.FATAL,
    'info': logging.INFO,
    'warning': logging.WARNING
}

if config.logging_level not in logging_levels.keys():
    logging_level = logging.INFO
else:
    logging_level = logging_levels[config.logging_level.lower()]

logging.basicConfig(level=logging_level, filename=config.log_file,
                    format='%(levelname)s:PID-%(process)d:%(asctime)s:%(message)s')

# Create output directory
if not os.path.exists(OUTPUT_DIRECTORY):
    os.mkdir(OUTPUT_DIRECTORY)

# Pull features
config.runtime_features_directory = os.path.join(OUTPUT_DIRECTORY, 'features')

if os.path.exists(config.runtime_features_directory):
    shutil.rmtree(config.runtime_features_directory)

proj_mgmt_authenticators = {
    'keyring': KeyringAuthenticator
}
proj_mgmt_authenticator = proj_mgmt_authenticators[config.proj_mgmt_authenticator](
    config=config.config_dict,
    system=config.proj_mgmt_class
    )

proj_mgmt_plugins = {
    'jira': JiraProjMgmtPlugin
}
proj_mgmt_plugin = proj_mgmt_plugins[config.proj_mgmt_class](
    config=config.config_dict,
    authenticator=proj_mgmt_authenticator,
    features_directory=config.runtime_features_directory
    )

os.makedirs(config.runtime_features_directory)

if config.download_feature_files:
    logging.info('Exporting feature files')
    proj_mgmt_plugin.export_feature_files()

if config.use_local_feature_files:
    logging.info('Copying feature files')
    feature_files = os.listdir(config.features_directory)
    for file in feature_files:
        if not file.endswith('.feature'):
            continue

        shutil.copyfile(
            os.path.join(config.features_directory, file),
            os.path.join(config.runtime_features_directory, file)
            )

# Execute tests
test_plugin_classes = {
    'behave': BehavePlugin
}

test_plugin = test_plugin_classes[config.test_class.lower()](config)
test_plugin.execute()

# Upload results
if config._upload_test_results:
    proj_mgmt_plugin.upload_test_results(test_plugin.test_results_file)

if __name__ == '__main__':
    pass
