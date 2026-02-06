# -*- coding: utf-8 -*-

import os
import shutil

from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterBoolean,
    QgsProcessingException,
    QgsProject,
    QgsVectorLayer
)
from PyQt5.QtCore import QStandardPaths


class InitModelRegistryAlgorithm(QgsProcessingAlgorithm):

    ADD_TO_PROJECT = "ADD_TO_PROJECT"

    def name(self):
        return "init_model_registry"

    def displayName(self):
        return "Create default model_registry"

    def group(self):
        return "Model Manager"

    def groupId(self):
        return "model_manager"

    def shortHelpString(self):
        return (
            "Copies the bundled model_registry.gpkg included in the plugin\n"
            "to the user's Downloads folder."
        )

    def createInstance(self):
        return InitModelRegistryAlgorithm()

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.ADD_TO_PROJECT,
                "Load into QGIS after creation",
                defaultValue=True
            )
        )

    def processAlgorithm(self, parameters, context, feedback):

        # --- Source (bundled in plugin)
        plugin_dir = os.path.dirname(__file__)
        src = os.path.join(plugin_dir, "data", "model_registry.gpkg")

        if not os.path.exists(src):
            raise QgsProcessingException(
                "Bundled model_registry.gpkg was not found"
            )

        # --- Destination (Downloads)
        download_dir = QStandardPaths.writableLocation(
            QStandardPaths.DownloadLocation
        )
        dst = os.path.join(download_dir, "model_registry.gpkg")

        if os.path.exists(dst):
            raise QgsProcessingException(
                f"File already exists:\n{dst}"
            )

        shutil.copy2(src, dst)
        feedback.pushInfo(f"Created: {dst}")

        # --- Load into QGIS (stable)
        if self.parameterAsBool(parameters, self.ADD_TO_PROJECT, context):
            uri = f"{dst}|layername=model_registry"
            layer = QgsVectorLayer(uri, "model_registry", "ogr")

            if layer.isValid():
                QgsProject.instance().addMapLayer(layer)
                feedback.pushInfo("model_registry has been added to QGIS")
            else:
                feedback.reportError(
                    "The GeoPackage was created, but could not be loaded into QGIS"
                )

        return {}
