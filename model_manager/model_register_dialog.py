# -*- coding: utf-8 -*-

import os
import shutil
from PyQt5.QtCore import QDate, QSettings

from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTextEdit,
    QFileDialog, QMessageBox
)
from qgis.core import (
    QgsProject,
    QgsApplication,
    QgsFeature
)


SETTINGS_KEY_SHARED_DIR = "model_manager/shared_models_dir"


class ModelRegisterDialog(QDialog):
    """
    Dialog to register a Processing model (.model3)

    1) Copy to processing/models
    2) Copy to a user-defined shared folder
    3) Insert a record into model_registry
    """

    def __init__(self, iface, parent=None):
        super().__init__(parent)
        self.iface = iface
        self.model_file = None

        self.setWindowTitle("Register Model")
        self.resize(520, 560)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.path_edit = QLineEdit()
        self.path_edit.setReadOnly(True)

        btn_sel = QPushButton("Select model3")
        btn_sel.clicked.connect(self.select_model)

        h = QHBoxLayout()
        h.addWidget(self.path_edit)
        h.addWidget(btn_sel)
        layout.addLayout(h)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Model name (Processing display name)")
        layout.addWidget(self.name_edit)

        self.layer_name_edit = QLineEdit()
        self.layer_name_edit.setPlaceholderText("Target layer name")
        layout.addWidget(self.layer_name_edit)

        self.tags_edit = QLineEdit()
        self.tags_edit.setPlaceholderText("Tags (optional)")
        layout.addWidget(self.tags_edit)

        self.note_edit = QTextEdit()
        self.note_edit.setPlaceholderText("Notes")
        layout.addWidget(self.note_edit)

        self.shared_dir_edit = QLineEdit()
        self.shared_dir_edit.setReadOnly(True)
        self.shared_dir_edit.setPlaceholderText("Shared model folder (not set)")

        btn_change = QPushButton("Set shared folder")
        btn_change.clicked.connect(self.change_shared_dir)

        h2 = QHBoxLayout()
        h2.addWidget(self.shared_dir_edit)
        h2.addWidget(btn_change)
        layout.addLayout(h2)

        self.load_shared_dir()

        btn = QPushButton("Register")
        btn.clicked.connect(self.register)
        layout.addWidget(btn)

    def select_model(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select model3",
            "",
            "Model (*.model3)"
        )
        if not path:
            return

        self.model_file = path
        self.path_edit.setText(path)

        base = os.path.splitext(os.path.basename(path))[0]
        self.name_edit.setText(base)

    def load_shared_dir(self):
        settings = QSettings()
        shared_dir = settings.value(SETTINGS_KEY_SHARED_DIR, "", type=str)
        if shared_dir and os.path.isdir(shared_dir):
            self.shared_dir_edit.setText(shared_dir)

    def change_shared_dir(self):
        shared_dir = QFileDialog.getExistingDirectory(
            self,
            "Select shared model folder",
            os.path.expanduser("~")
        )
        if not shared_dir:
            return

        settings = QSettings()
        settings.setValue(SETTINGS_KEY_SHARED_DIR, shared_dir)

        self.shared_dir_edit.setText(shared_dir)

        QMessageBox.information(
            self,
            "Shared Folder",
            f"Shared folder has been set:\n{shared_dir}"
        )

    def get_shared_dir(self):
        settings = QSettings()
        shared_dir = settings.value(SETTINGS_KEY_SHARED_DIR, "", type=str)
        if not shared_dir or not os.path.isdir(shared_dir):
            return None
        return shared_dir

    def register(self):
        if not self.model_file:
            QMessageBox.warning(self, "Register", "Please select a model3 file")
            return

        model_name = self.name_edit.text().strip()
        if not model_name:
            QMessageBox.warning(self, "Register", "Model name is required")
            return

        shared_dir = self.get_shared_dir()
        if not shared_dir:
            QMessageBox.warning(self, "Register", "Shared folder is not configured")
            return

        models_dir = os.path.join(
            QgsApplication.qgisSettingsDirPath(),
            "processing",
            "models"
        )
        os.makedirs(models_dir, exist_ok=True)

        src = os.path.abspath(self.model_file)
        dst = os.path.join(models_dir, os.path.basename(self.model_file))

        if src != os.path.abspath(dst):
            shutil.copy2(src, dst)

        shared_dst = os.path.join(shared_dir, os.path.basename(self.model_file))
        if src != os.path.abspath(shared_dst):
            shutil.copy2(src, shared_dst)

        layers = QgsProject.instance().mapLayersByName("model_registry")
        if not layers:
            QMessageBox.critical(self, "Register", "model_registry layer not found")
            return

        layer = layers[0]

        if not layer.startEditing():
            QMessageBox.critical(self, "Register", "Failed to start editing the layer")
            return

        today = QDate.currentDate()

        feat = QgsFeature(layer.fields())
        feat["model_name"] = model_name
        feat["layer_name"] = self.layer_name_edit.text()
        feat["model_path"] = f"model:{model_name}"
        feat["tags"] = self.tags_edit.text()
        feat["note"] = self.note_edit.toPlainText()
        feat["created_at"] = today
        feat["updated_at"] = today

        ok = layer.addFeature(feat)
        if not ok:
            layer.rollBack()
            QMessageBox.critical(self, "Register", "addFeature failed")
            return

        if not layer.commitChanges():
            QMessageBox.critical(self, "Register", "commitChanges failed")
            return

        layer.triggerRepaint()
        layer.reload()

        QMessageBox.information(self, "Register", "Model has been registered successfully")
        self.accept()
