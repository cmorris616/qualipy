# QualiPy
QualiPy is a framework for assisting with the automated testing process.  Qualipy is not meant to replace pytest, behave, or other testing frameworks.  Instead, it is meant to augment the process to provider further automation.  It can be configured based on the needs of the project and the availablility of other technologies.

QualiPy features include:
- Exporting feature files from JIRA for progression and regression testing
- Uploading test results to JIRA
- Moving user stories based on test results]
- Loading test data to be used during the testing process
- Data management across steps and scenarios

## Test Plugins
QualiPy is built to use multiple testing frameworks via plugins.  Currently, QualiPy only supports the behave framework for business-driven development.

## Project Management Plugins
Like the testing plugins, QualiPy can also use multiple project management software suites (such as JIRA) via plugins.

### Authentication
In most cases, authentication needs to happen in order to interact with project management software suites.  This interaction can use certificates, API keys, or simple username/password combinations.  The difficult part is how to secure the credentials.  For starters, a keyring authenticator is implemented that just uses the keyring functionality for the underlying OS.

## Initial Setup
**In order to test using JIRA, you must have a running JIRA instance.**
1. Create a test project that uses behave to run tests from feature files
1. Create and activate a virtual environment (optional)
1. Install QualiPy (`pip install qualipy`)
1. Execute QualiPy (`python -m qualipy`)

QualiPy looks for **qualipy.yaml** in the current directory.  If that is not found, then default configuration settings are used.  Additionally, other YAML config files can be used by including the **--config-file** command line argument. 

QualiPy assumes that the feature files are located in the **features** directory in the current working directory.  This can be changed with the **--features-dir** command line argument.