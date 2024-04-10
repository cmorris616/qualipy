# Settings

Settings will be read from qualipy.yaml by default, but can be overridden by using the **&dash;&dash;config-file** argument on the command line.

## General

- **download.feature.files**
    - Whether or not to download feature files from a project management suite.  Valid values are `true` and `false`.
    - Default value: `false`
- **failed.story.status**
    - The status to which a story should be moved when one or more of the attached tests fails
    - Default value: `In Progress`
- **features.directory**
    - The directory where the feature files are stored
    - Default value: `features`
    - Command Line Override: `--features_dir [desired directory]`
- **logging.level**
    - The level of logging to be maintained during execution.  Valid values are `critical`, `debug`, `error`, `fatal`, `info`, and `warning`.
    - Default value: `info`
- **move.user.stories**
    - Indicates whether or not user stories should be moved after testing.  This only applies when progression testing
    - Default value: `False`
- **output.directory**
    - The location in which to place output files such as test reports.
    - Default value: `qualipy_output`
    - Command Line Override: `--output_dir [desired directory]`
- **project.management.authenticator.class**
    - The fully qualified class name to be used for authentication
    - Default value: `qualipy.authentication.keyring_authenticator.KeyringAuthenticator`
- **project.management.plugin**
    - The fully qualified class name to be used for project management
    - Default value: `qualipy.proj_mgmt_plugins.jira_proj_mgmt_plugin.JiraProjMgmtPlugin`
- **project.management**
    - The system name used when reading credentials from the OS keyring
    - Default value: `project.management`
- **success.story.status**
    - The status to which a story should be moved when all the attached tests succeed
    - Default value: `Done`
- **test.plugin**
    - The fully qualified class name used for testing
    - Default value: `qualipy.test_plugins.behave_plugin.BehavePlugin`
- **testing.type**
    - The type of testing taking place.  Valid values are `progression` and `regression`.  This determines how the project management plugin behaves when retrieving tests and uploading results.
    - Default value: `regression`
- **upload.test.results**
    - Whether or not to upload test results upon completion of the testing process.  Valid values are `true` and `false`.
    - Default value: `false`
- **use.access.token**
    - Whether or not to use an access token when authenticating to a project management suite.  Valid values are `true` and `false`.
    - Default value: `true`
- **use.local.feature.files**
    - Whether or not to use local feature files.  Valid values are `true` and `false`.
    - Default value: `true`
