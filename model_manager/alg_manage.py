from qgis.core import QgsProcessingAlgorithm
from qgis.utils import iface

from .model_manager_dialog import ModelManageDialog


class ModelManageAlgorithm(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        # Required even if there are no parameters
        pass

    def name(self):
        return "model_manage"

    def displayName(self):
        return "Model Manager (List & Run)"

    def group(self):
        return "Model Manager"

    def groupId(self):
        return "model_manager"

    def shortHelpString(self):
        return "Displays a list of registered Processing models and allows execution."

    def createInstance(self):
        return ModelManageAlgorithm()

    def processAlgorithm(self, parameters, context, feedback):
        dlg = ModelManageDialog(iface)
        dlg.exec_()
        return {}
