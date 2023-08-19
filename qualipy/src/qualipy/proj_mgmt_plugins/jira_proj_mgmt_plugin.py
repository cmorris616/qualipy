import json
import logging
import os
import tempfile
from zipfile import ZipFile
import requests
import base64
from qualipy.exceptions.app_exceptions import HttpException, InvalidTestingTypeError, MissingUrlError
from .proj_mgmt_plugin import TESTING_TYPE_PROGRESSION, TESTING_TYPE_REGRESSION, ProjMgmtPlugin

# JSON keys/field names
DESCRIPTION_KEY = 'description'
FIELDS_KEY = 'fields'
ID_FIELD = 'id'
INWARD_ISSUE_KEY = 'inwardIssue'
INWARD_KEY = 'inward'
ISSUES_KEY = 'issues'
ISSUE_KEY_FIELD = 'key'
ISSUE_LINKS_FIELD = 'issuelinks'
NAME_FIELD = 'name'
PROJECT_FIELD = 'project'
TESTED_BY_VALUE = 'tested by'
TOTAL_ISSUES_KEY = 'total'
TYPE_KEY = 'type'

# API Paths
ISSUE_SEARCH_PATH = '/rest/api/2/search'
PROJECT_SEARCH_PATH = '/rest/api/2/project'
TEST_EXPORT_PATH = '/rest/raven/1.0/export/test'
TEST_RESULTS_IMPORT_PATH = '/rest/raven/1.0/import/execution/behave/multipart'


class JiraProjMgmtPlugin(ProjMgmtPlugin):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._regression_test_query = self._config.get(
            'jira.regression.test.query', 'type=Test')
        self._progression_test_query = self._config.get(
            'jira.progression.test.query', 'type=Story and status=Test')
        self._jira_url = self._config.get('jira.url', '')
        self._max_results = self._config.get('jira.max.results', 1000)
        self._features_directory = kwargs.get('features_directory', 'features')
        self._project_key = self._config.get('jira.project.key', '')
        self._test_execution_info = self._config.get(
            'jira.test.execution.info', None)
        self._jira_project = None

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
        logging.info('Exporting progression tests from JIRA')
        logging.info('Querying for user stories')
        stories = self._query_issues(self._progression_test_query)

        issue_keys = []

        for story in stories:
            linked_issues = story[FIELDS_KEY][ISSUE_LINKS_FIELD]

            for linked_issue in linked_issues:
                if TYPE_KEY not in linked_issue.keys():
                    continue

                if INWARD_KEY not in linked_issue[TYPE_KEY].keys():
                    continue

                if linked_issue[TYPE_KEY][INWARD_KEY] != TESTED_BY_VALUE:
                    continue

                issue_keys.append(
                    linked_issue[INWARD_ISSUE_KEY][ISSUE_KEY_FIELD])
                
        if len(issue_keys) == 0:
            logging.info('No tests found in JIRA')
            return

        # Send request for feature files
        issue_list = ';'.join(issue_keys)
        response = requests.get(
            url=f'{self._jira_url}{TEST_EXPORT_PATH}?keys={issue_list}&fz=true',
            headers=self._get_request_headers()
        )

        if response.status_code != 200:
            raise HttpException(
                'An error occurred while attempting to export progression tests', response=response)

        with tempfile.NamedTemporaryFile(mode='w+b', suffix='.zip') as temp_file:
            temp_file.write(response.content)
            temp_file.seek(0)

            with ZipFile(temp_file.name, 'r') as zip_file:
                zip_file.extractall(path=self._features_directory)

    def _export_regression_tests(self):
        logging.info('Exporting regression tests from JIRA')
        issues = self._query_issues(self._regression_test_query)

        if issues is None or len(issues) == 0:
            logging.info('No regression tests found')
            return

        # Send request for feature files
        issue_list = ';'.join([x[ISSUE_KEY_FIELD] for x in issues])
        response = requests.get(
            url=f'{self._jira_url}{TEST_EXPORT_PATH}?keys={issue_list}&fz=true',
            headers=self._get_request_headers()
        )

        if response.status_code != 200:
            raise HttpException(
                'An error occurred while attempting to export regression tests', response=response)

        with tempfile.NamedTemporaryFile(mode='w+b', suffix='.zip') as temp_file:
            temp_file.write(response.content)
            temp_file.seek(0)

            with ZipFile(temp_file.name, 'r') as zip_file:
                zip_file.extractall(path=self._features_directory)

    def _get_jira_project(self):
        if self._jira_project is not None:
            return self._jira_project

        if self._project_key == '':
            logging.warning('No JIRA project key set.  Unable to retrieve project info.')
            return None

        response = requests.get(url=f'{self._jira_url}{PROJECT_SEARCH_PATH}/{self._project_key}',
                                headers=self._get_request_headers())
        
        if response.status_code != 200:
            raise HttpException('An error occurred while retrieving project info', response)
        
        response_dict = json.loads(response.content.decode())

        self._jira_project = {
            ID_FIELD: response_dict[ID_FIELD],
            NAME_FIELD: response_dict[NAME_FIELD],
            ISSUE_KEY_FIELD: response_dict[ISSUE_KEY_FIELD],
            DESCRIPTION_KEY: response_dict[DESCRIPTION_KEY]
        }

        return self._jira_project

    def _get_request_headers(self):
        if self._use_access_token:
            logging.debug('Using access token to connect to JIRA')
            auth_header_value = f'Bearer {self._authenticator.get_api_key()}'
        else:
            logging.debug('Using username and password to connect to to JIRA')
            auth_header_value = 'Basic ' + base64.b64encode(
                f'{self._authenticator.get_username()}:{self._authenticator.get_password()}'
                .encode('utf-8')).decode('utf-8')

        return {
            'Authorization': auth_header_value,
            'Content-Type': 'application/json'
        }

    def _query_issues(self, jql):
        # Get credentials and set the authorization header
        headers = self._get_request_headers()

        start_item = 0
        expected_issue_count = self._max_results
        issues = []

        while len(issues) < expected_issue_count:
            # Send JQL query
            target_url = f'{self._jira_url}{ISSUE_SEARCH_PATH}'
            body = {
                'jql': jql,
                'startAt': start_item,
                'maxResults': self._max_results,
                'fields': [
                    ISSUE_KEY_FIELD,
                    ISSUE_LINKS_FIELD,
                    PROJECT_FIELD
                ]
            }
            response = requests.post(
                url=target_url, headers=headers, json=body)

            if response.status_code != 200:
                raise HttpException(
                    'An error occurred while attempting to query issues', response=response)

            response_dict = json.loads(response.content.decode())
            issues = issues + response_dict[ISSUES_KEY]
            expected_issue_count = response_dict[TOTAL_ISSUES_KEY]
            start_item += 1

            if self._project_key == '' and len(issues) > 0:
                self._project_key = issues[0][FIELDS_KEY][PROJECT_FIELD][ISSUE_KEY_FIELD]

        return issues

    def upload_test_results(self, test_results_file):

        if self._get_jira_project() is None:
            logging.error('JIRA project info not available.  Unable to upload results.')
            return

        logging.info('Uploading test results')
        headers = self._get_request_headers()
        del headers['Content-Type']

        if self._test_execution_info is None:
            self._test_execution_info = {
                'fields': {
                    'project': self._get_jira_project(),
                    'summary': f'{self._jira_project[NAME_FIELD]} {self._testing_type.title()} Test Execution'
                }
            }

        proj_info_filename = os.path.join(self._config['output.directory'], 'proj_info.json')
        
        with open(proj_info_filename, 'w') as proj_info_file:
            proj_info_file.write(json.dumps(self._test_execution_info))
        
        with open(proj_info_filename, 'r') as proj_file, open(test_results_file, 'r') as results_file:
            response = requests.post(
                url=f'{self._jira_url}{TEST_RESULTS_IMPORT_PATH}',
                headers=headers,
                files={'info': proj_file, 'result': results_file})

            if response.status_code != 200:
                raise HttpException('An error occurred while uploading test results', response)
