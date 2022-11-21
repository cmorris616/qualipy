import argparse
import logging

from config import get_config, load_config
from proj_mgmt_plugins.jira_proj_mgmt_plugin import JiraProjMgmtPlugin
from test_plugins.behave_plugin import BehavePlugin

parser = argparse.ArgumentParser(
    prog='PyTF - Python Testing Framework',
    description='Adds automation to the testing process'
)

parser.add_argument('--config-file', default='pytf.yaml')
parser.add_argument('--features-dir')

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

# Pull features
logging.info('Exporting feature files')
proj_mgmt_plugins = {
    'jira': JiraProjMgmtPlugin
}
proj_mgmt_plugin = proj_mgmt_plugins[config.proj_mgmt_class](config)
proj_mgmt_plugin.export_feature_files()

# Execute tests
test_plugin_classes = {
    'behave': BehavePlugin
}

test_plugin = test_plugin_classes[config.test_class.lower()](config)
test_plugin.execute()

# Upload results

if __name__ == '__main__':
    pass
