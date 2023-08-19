from unittest import TestCase

from qualipy.proj_mgmt_plugins.proj_mgmt_plugin import ProjMgmtPlugin


class TestProjMgmtPlugin(TestCase):
    def test_export_feature_files(self):
        plugin = ProjMgmtPlugin()
        self.assertRaises(NotImplementedError, plugin.export_feature_files)

    def test_upload_test_results(self):
        plugin = ProjMgmtPlugin()
        self.assertRaises(NotImplementedError, plugin.upload_test_results, None)