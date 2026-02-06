from qgis.core import QgsProcessingAlgorithm
from qgis.utils import iface

from .model_register_dialog import ModelRegisterDialog


class ModelRegisterAlgorithm(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        # Required even if there are no parameters
        pass

    def name(self):
        return "model_register"

    def displayName(self):
        return "Model Register (Register model3)"

    def group(self):
        return "Model Manager"

    def groupId(self):
        return "model_manager"

    def shortHelpString(self):
        return "Registers a Processing model (.model3) and adds it to the model registry."

    def createInstance(self):
        return ModelRegisterAlgorithm()

    def processAlgorithm(self, parameters, context, feedback):
        dlg = ModelRegisterDialog(iface)
        dlg.exec_()
        return {}
