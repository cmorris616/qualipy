# JIRA
QualiPy can interact with JIRA to retrieve tests (if JIRA uses the Xray plugin) and upload the test results.

## Credentials
The credentials are stored with a service name of **jira**.  For more information, see [Credentials](credentials.md)

## Settings
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
