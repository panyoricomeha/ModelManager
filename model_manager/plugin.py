# -*- coding: utf-8 -*-

from qgis.core import QgsApplication
from .provider import ModelManagerProvider


class ModelManagerPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.provider = None

    def initGui(self):

        self.provider = ModelManagerProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def unload(self):
        if self.provider:
            QgsApplication.processingRegistry().removeProvider(self.provider)
