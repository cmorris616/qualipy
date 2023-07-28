# Settings

Settings will be read from pytf.yaml by default, but can be overridden by using the `--config-file` argument on the command line.

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
- **upload.test.results**
    - Whether or not to upload test results upon completion of the testing process.  Valid values are `true` and `false`.
    - Default value: `false`
- **use.access.token**
    - Whether or not to use an access token when authenticating to a project management suite.  Valid values are `true` and `false`.
    - Default value: `true`
- **use.local.feature.files**
    - Whether or not to use local feature files.  Valid values are `true` and `false`.
    - Default value: `true`

## JIRA

The following settings are used by the JIRA project management plugin.  The use of JIRA assumes the use of the XRay plugin for testing.

- **jira.max.results**
    - The maximum number of records to be returned from JIRA when a query is executed
    - Default value: 1000
- **jira.progression.test.query**
    - The JQL query that is used to retrieve user stories with attached tests
    - Default value: blank
    - Example value: `'type=Story and status=Testing'`
- **jira.project.key**
    - The JIRA project key for your JIRA project
    - Default value: blank
- **jira.regression.test.query**
    - The JQL query that is to be used to retrieve tests from JIRA
    - Default value: blank
    - Example value: `jira.regression.test.query: 'type=Test'`
- **jira.test.execution.info**
    - JSON containing test execution data for newly created test executions
    - Default value:

            {
                'fields': {
                    'project': *[JIRA project based on the jira.project.key]*,
                    'summary': *[JIRA project name] [testing type]* Test Execution'
            }
- **jira.url**
    - The URL for the JIRA instance being used
    - Default value: blank
    - Example value: `'http://myjirainstance.internal'`
