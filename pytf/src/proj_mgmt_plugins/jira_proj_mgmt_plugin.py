import json
import logging
import tempfile
from zipfile import ZipFile
import requests
import base64
from exceptions.app_exceptions import InvalidTestingTypeError, MissingUrlError
from .proj_mgmt_plugin import TESTING_TYPE_PROGRESSION, TESTING_TYPE_REGRESSION, ProjMgmtPlugin

ID_FIELD = 'id'
ISSUES_KEY = 'issues'
ISSUE_KEY_FIELD = 'key'
ISSUE_SEARCH_PATH = '/rest/api/2/search'
TEST_EXPORT_PATH = '/rest/raven/1.0/export/test'
TOTAL_ISSUES_KEY = 'total'

class JiraProjMgmtPlugin(ProjMgmtPlugin):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._use_access_token = kwargs.get('use_access_token', 'true').lower() == 'true'
        self._regression_test_query = self._config.get('jira.regression.test.query', 'type=Test')
        self._jira_url = self._config.get('jira.url', '')
        self._max_results = self._config.get('jira.max.results', 1000)
        self._features_directory = kwargs.get('features_directory', 'features')

        if self._jira_url.strip() == '':
            logging.warning(msg='No JIRA URL is set')

    def export_feature_files(self):
        if self._jira_url.strip() == '':
            logging.error('No JIRA URL is set')
            raise MissingUrlError()

        if self._testing_type == TESTING_TYPE_REGRESSION:
            self._export_regression_tests()
        elif self._testing_type == TESTING_TYPE_PROGRESSION:
            self._export_progression_tests()
        else:
            raise InvalidTestingTypeError(self._testing_type)
        
    def _export_progression_tests(self):
        pass

    def _export_regression_tests(self):
        # Get credentials and set the authorization header
        headers = {
            'Authorization': 'Basic ' + base64.b64encode(
                f'{self._authenticator.get_username()}:{self._authenticator.get_password()}'
                .encode('utf-8')).decode('utf-8'),
            'Content-Type': 'application/json'
        }

        start_item = 0
        expected_issue_count = self._max_results
        issues = []

        while len(issues) < expected_issue_count:
            # Send JQL query
            target_url = f'{self._jira_url}{ISSUE_SEARCH_PATH}'
            body = {
                'jql': self._regression_test_query,
                'startAt': start_item,
                'maxResults': self._max_results,
                'fields': [ISSUE_KEY_FIELD]
            }
            response = requests.post(url=target_url, headers=headers, json=body)

            response_dict = json.loads(response.content.decode())
            issues = issues + response_dict[ISSUES_KEY]
            expected_issue_count = response_dict[TOTAL_ISSUES_KEY]
            start_item += 1

        # Send request for feature files
        issue_list = ';'.join([x[ISSUE_KEY_FIELD] for x in issues])
        response = requests.get(
            url=f'{self._jira_url}{TEST_EXPORT_PATH}?keys={issue_list}&fz=true',
            headers=headers
            )
        
        with tempfile.NamedTemporaryFile(mode='w+b', suffix='.zip') as temp_file:
            temp_file_name = temp_file.name
            temp_file.write(response.content)
            temp_file.seek(0)

            with ZipFile(temp_file.name, 'r') as zip_file:
                zip_file.extractall(path=self._features_directory)

    def _get_user_stories(self):
        pass
