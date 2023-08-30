# Plugin Development
If you are not using JIRA, Behave, and/or the OS keyring, you can use third-party plugins or create your own plugins to customize the functionality of {{projectName}}.  {{projectName}} supports plugins for project management, authentication, and testing.  Out of the box, {{projectName}} has a plugin for JIRA for project management, keyring authentication, and Behave for testing.

In order to create plugins, simply create a class that implements the methods of the appropriate parent class and update the corresponding setting in your configuration (see [settings](/settings.md)).  See the below for the functionality to be implemented.

## Project Management Plugin
Associated setting (**project.management.plugin**)
```
# qualipy.proj_mgmt_plugins.proj_mgmt_plugin

class ProjMgmtPlugin:
    def __init__(self, **kwargs):
        self._authenticator = kwargs.get('authenticator', None)
        self._config = kwargs.get('config', {})
        self._testing_type = self._config.get(
            'testing.type', TESTING_TYPE_REGRESSION)
        self._use_access_token = self._config.get('use.access.token', True)
        self._upload_test_results = self._config.get('upload.test.results', True)

    @abc.abstractmethod
    def export_feature_files(self):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def upload_test_results(self, test_results_file):
        raise NotImplementedError()
```

## Authentication Plugin
Associated setting (**project.management.authenticator.class**)
```
# qualipy.authentication.authenticator

class Authenticator:
    def __init__(self, **kwargs):
        pass
    
    @abc.abstractmethod
    def get_username(self):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def get_password(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_api_key(self):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def get_certificate(self):
        raise NotImplementedError()
```

## Testing Plugin
Associated setting (**test.plugin**)
```
# qualipy.test_plugins.test_plugin

class TestPlugin(abc.ABC):

    def __init__(self, config: AppConfig):
        self._config = config
    
    @abc.abstractmethod
    def execute(self):
        raise NotImplementedError()
    
    @abc.abstractproperty
    def test_results_file(self):
        raise NotImplementedError()
```