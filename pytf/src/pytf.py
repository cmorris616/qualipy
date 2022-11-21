import argparse

from config import get_config, load_config
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

# Pull features

# Execute tests
test_plugin_classes = {
    'behave': BehavePlugin
}

# test_class = test_plugin_classes[config.test_class.lower()]()
test_class = BehavePlugin()
test_class.execute(config)

# Upload results

if __name__ == '__main__':
    pass
