from .proj_mgmt_plugin import ProjMgmtPlugin


class JiraProjMgmtPlugin(ProjMgmtPlugin):
    def export_feature_files(self):
        self._config
