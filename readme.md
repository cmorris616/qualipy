# QualiPy
QualiPy is a framework for assisting with the automated testing process.  Qualipy is not meant to replace pytest, behave, or other testing frameworks.  Instead, it is meant to augment the process to provider further automation.  It can be configured based on the needs of the project and the availablility of other technologies.

QualiPy features include:
- Exporting feature files from JIRA for progression and regression testing
- Uploading test results to JIRA

Coming Soon:
- Moving user stories based on the outcome of the tests
- Loading test data to be used during the testing process
- Cleaning up the test data after the testing has completed
- Data management across steps and scenarios

## Test Plugins
QualiPy is built to use multiple testing frameworks via plugins.  Currently, QualiPy only supports the behave framework for business-driven development.

## Project Management Plugins
Like the testing plugins, QualiPy can also use multiple project management software suites (such as JIRA) via plugins.

### Authentication
In most cases, authentication needs to happen in order to interact with project management software suites.  This interaction can use certificates, API keys, or simple username/password combinations.  The difficult part is how to secure the credentials.  For starters, a keyring authenticator is implemented that just uses the keyring functionality for the underlying OS.

## Initial Setup
**In order to test using JIRA, you must have a running JIRA instance.**
If you are using Linux, there is a 'run.sh' file that will handle cleaning, building, installing, and running tests using QualiPy and the QualiPy test project.  If you are not using Linux, follow the below steps.

1. Clone the repository
1. Change to the root directory of the project
1. **Optional** Create and activate a virtual environment
1. Execute `pip install -r requirements`
1. Change to the `qualipy` folder
1. Ensure that the `dist` folder is removed (or at least empty)
1. Execute `python -m build`
1. Ensure that QualiPy is not currently installed by executing `pip uninstall -y qualipy`
1. Install the newly built wheel file by executing `pip install dist/qualipy-*-py3-none-any.whl`
1. Change to the qualipy-test directory
1. Execute `python -m qualipy`