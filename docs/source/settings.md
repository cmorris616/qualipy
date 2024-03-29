# Settings

Settings will be read from qualipy.yaml by default, but can be overridden by using the **&dash;&dash;config-file** argument on the command line.

## General

- **download.feature.files**
    - Whether or not to download feature files from a project management suite.  Valid values are `true` and `false`.
    - Default value: `false`
- **logging.level**
    - The level of logging to be maintained during execution.  Valid values are `critical`, `debug`, `error`, `fatal`, `info`, and `warning`.
    - Default value: `info`
- **testing.type**
    - The type of testing taking place.  Valid values are `progression` and `regression`.  This determines how the project management plugin behaves when retrieving tests and uploading results.
    - Default value: `regression`
- **project.management.authenticator.class**
    - The fully qualified class name to be used for authentication
    - Default value: `qualipy.authentication.keyring_authenticator.KeyringAuthenticator`
- **project.management.plugin**
    - The fully qualified class name to be used for project management
    - Default value: `qualipy.proj_mgmt_plugins.jira_proj_mgmt_plugin.JiraProjMgmtPlugin`
- **project.management**
    - The system name used when reading credentials from the OS keyring
    - Default value: `project.management`
- **test.plugin**
    - The fully qualified class name used for testing
    - Default value: `qualipy.test_plugins.behave_plugin.BehavePlugin`
- **upload.test.results**
    - Whether or not to upload test results upon completion of the testing process.  Valid values are `true` and `false`.
    - Default value: `false`
- **use.access.token**
    - Whether or not to use an access token when authenticating to a project management suite.  Valid values are `true` and `false`.
    - Default value: `true`
- **use.local.feature.files**
    - Whether or not to use local feature files.  Valid values are `true` and `false`.
    - Default value: `true`
