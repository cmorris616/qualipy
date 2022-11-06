# PyTF
## **This readme is based on the current plan for PyTF, not the current state of the project**
PyTF (Python Testing Framework) is a framework for assisting with the automated testing process.
PyTF is not meant to replace pytest, behave, or other testing frameworks.  Instead, it is meant to
augment the process to provider further automation.  It can be configured based on the needs of the project and the availablility of other technologies.

PyTF features include:
- Exporting feature files from JIRA for progression and regression testing
- Loading test data to be used during the testing process
- Cleaning up the test data after the testing has completed
- Uploading test results to JIRA
- Moving user stories based on the outcome of the tests