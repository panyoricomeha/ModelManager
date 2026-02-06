# -*- coding: utf-8 -*-

from qgis.core import QgsProcessingProvider
from .alg_manage import ModelManageAlgorithm
from .alg_register import ModelRegisterAlgorithm
from .alg_init_registry import InitModelRegistryAlgorithm


class ModelManagerProvider(QgsProcessingProvider):

    def id(self):
        return "model_manager"

    def name(self):
        return "Model Manager"

    def longName(self):
        return "Model Manager Tools"

    def loadAlgorithms(self):
        self.addAlgorithm(ModelManageAlgorithm())
        self.addAlgorithm(ModelRegisterAlgorithm())
        self.addAlgorithm(InitModelRegistryAlgorithm())
