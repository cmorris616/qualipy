from unittest import TestCase
from unittest.mock import Mock, mock_open, patch

from pytest import MonkeyPatch
from qualipy.exceptions.app_exceptions import HttpException, InvalidTestingTypeError, MissingUrlError

from qualipy.proj_mgmt_plugins.jira_proj_mgmt_plugin import JiraProjMgmtPlugin


class TestJiraProjMgmtPlugin(TestCase):
    @patch('logging.warning')
    def test_init(self, logging_mock):
        JiraProjMgmtPlugin()
        logging_mock.assert_called_with(msg='No JIRA URL is set')

    def test_export_feature_files(self):
        queryIssuesResponse = Mock()
        testExportResponse = Mock()
        monkeypatch = MonkeyPatch()

        queryIssuesResponse.status_code = 200
        queryIssuesResponse.content = b'{"issues":[],"total":0}'

        testExportResponse.status_code = 200
        testExportResponse.content = b''

        monkeypatch.setattr('requests.post', lambda url, headers, json: queryIssuesResponse)
        monkeypatch.setattr('requests.get', lambda url, headers: testExportResponse)

        pm_plugin = JiraProjMgmtPlugin()
        self.assertRaises(MissingUrlError, pm_plugin.export_feature_files)

        config = {}
        config['jira.url'] = 'http://jiraurl'
        config['testing.type'] = 'badtestingtype'

        pm_plugin = JiraProjMgmtPlugin(config=config)
        self.assertRaises(InvalidTestingTypeError, pm_plugin.export_feature_files)

    def test_export_feature_files_regression(self):
        queryIssuesResponse = Mock()
        testExportResponse = Mock()
        monkeypatch = MonkeyPatch()

        queryIssuesResponse.status_code = 400
        queryIssuesResponse.content = b'{"issues":[],"total":0}'

        testExportResponse.status_code = 400
        testExportResponse.content = b''

        monkeypatch.setattr('requests.post', lambda url, headers, json: queryIssuesResponse)
        monkeypatch.setattr('requests.get', lambda url, headers: testExportResponse)

        pm_plugin = JiraProjMgmtPlugin()
        config = {}

        config['jira.url'] = 'http://jiraurl'
        config['testing.type'] = 'regression'
        authenticator = Mock()
        authenticator.get_api_key = lambda: 'test_api_key'

        pm_plugin = JiraProjMgmtPlugin(config=config, authenticator=authenticator)
        self.assertRaises(HttpException, pm_plugin.export_feature_files)

        queryIssuesResponse.status_code = 200
        pm_plugin.export_feature_files()

        queryIssuesResponse.content = b'{' \
        b'"issues":[' \
        b'{"key": "123","fields":{"project":{"key":"projectkey"}}},' \
        b'{"key": "456","fields":{"project":{"key":"projectkey"}}}' \
        b'],"total":2}'

        self.assertRaises(HttpException, pm_plugin.export_feature_files)
        testExportResponse.status_code = 200

        zip_bytes = None
        with open('tests/export.zip', 'rb') as zipfile:
            zip_bytes = zipfile.read()

        testExportResponse.content = zip_bytes

        pm_plugin = JiraProjMgmtPlugin(config=config, authenticator=authenticator)
        pm_plugin.export_feature_files()

    def test_export_feature_files_progression(self):
        queryIssuesResponse = Mock()
        testExportResponse = Mock()
        monkeypatch = MonkeyPatch()

        queryIssuesResponse.status_code = 400
        queryIssuesResponse.content = b'{"issues":[],"total":0}'

        testExportResponse.status_code = 400
        testExportResponse.content = b''

        monkeypatch.setattr('requests.post', lambda url, headers, json: queryIssuesResponse)
        monkeypatch.setattr('requests.get', lambda url, headers: testExportResponse)

        pm_plugin = JiraProjMgmtPlugin()
        config = {}

        config['jira.url'] = 'http://jiraurl'
        config['testing.type'] = 'progression'
        authenticator = Mock()
        authenticator.get_api_key = lambda: 'test_api_key'

        pm_plugin = JiraProjMgmtPlugin(config=config, authenticator=authenticator)
        self.assertRaises(HttpException, pm_plugin.export_feature_files)

        queryIssuesResponse.status_code = 200
        pm_plugin.export_feature_files()

        queryIssuesResponse.content = b'{' \
        b'"issues":[' \
        b'{"key": "123","fields":{"project":{"key":"projectkey"},"issuelinks": []}},' \
        b'{"key": "345","fields":{"project":{"key":"projectkey"},"issuelinks": [{}]}},' \
        b'{"key": "456","fields":{"project":{"key":"projectkey"},"issuelinks": [{"type": {}}]}},' \
        b'{"key": "789","fields":{"project":{"key":"projectkey"},"issuelinks": ' \
            b'[{"type": {"inward":"tested by"},"inwardIssue":{"key":"inwardkey"}}]}},' \
        b'{"key": "234","fields":{"project":{"key":"projectkey"},"issuelinks": [{"type": {"inward":"cloned by"}}]}}' \
        b'],"total":4}'

        self.assertRaises(HttpException, pm_plugin.export_feature_files)
        testExportResponse.status_code = 200

        zip_bytes = None
        with open('tests/export.zip', 'rb') as zipfile:
            zip_bytes = zipfile.read()

        testExportResponse.content = zip_bytes

        pm_plugin = JiraProjMgmtPlugin(config=config, authenticator=authenticator)
        pm_plugin.export_feature_files()

    def test_upload_results(self):
        config = {}
        monkeypatch = MonkeyPatch()

        config['jira.url'] = 'http://jiraurl'
        config['testing.type'] = 'progression'
        config['use.access.token'] = False
        config['output.directory'] = ''
        authenticator = Mock()
        authenticator.get_username = lambda: 'test_username'
        authenticator.get_password = lambda: 'test_password'
        pm_plugin = JiraProjMgmtPlugin(config=config, authenticator=authenticator)
        pm_plugin.upload_test_results('')

        projectQueryResponse = Mock()
        projectQueryResponse.status_code = 400

        resultsUploadResponse = Mock()
        resultsUploadResponse.status_code = 200

        monkeypatch.setattr('requests.get', lambda url, headers: projectQueryResponse)
        monkeypatch.setattr('requests.post', lambda url, headers, files: resultsUploadResponse)

        config['jira.project.key'] = 'projectkey'

        pm_plugin = JiraProjMgmtPlugin(config=config, authenticator=authenticator)
        self.assertRaises(HttpException, pm_plugin.upload_test_results, '')

        projectQueryResponse.status_code = 200
        projectQueryResponse.content = b'{"id":"123","name":"testproject","key":"projectkey","description":""}'

        with patch('builtins.open', mock_open(read_data='[]')) as mock_open_file:
            pm_plugin.upload_test_results('test_results_file')
            resultsUploadResponse.status_code = 404
            self.assertRaises(HttpException, pm_plugin.upload_test_results, 'test_results_file')