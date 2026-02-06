# -*- coding: utf-8 -*-

from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit,
    QMessageBox, QTableView
)
from qgis.core import QgsProject
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
from PyQt5.QtCore import Qt
import processing

from .memo_confirm_dialog import MemoConfirmDialog


class ModelManageDialog(QDialog):

    def __init__(self, iface, parent=None):
        super().__init__(parent)

        self.iface = iface
        self.layer = None
        self.rows = []  # [(feature, exists)]

        self.setWindowTitle("Model Manager (List & Run)")
        self.resize(1000, 560)

        self.init_ui()
        self.reload_all()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.search = QLineEdit()
        self.search.setPlaceholderText(
            "Search (Model name / Layer / Tags / Note)"
        )
        self.search.textChanged.connect(self.apply_filter)
        layout.addWidget(self.search)

        self.table = QTableView()
        self.table.doubleClicked.connect(self.on_double_click)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)
        self.table.setEditTriggers(QTableView.NoEditTriggers)
        layout.addWidget(self.table)

    def reload_all(self):
        layers = QgsProject.instance().mapLayersByName("model_registry")
        if not layers:
            QMessageBox.warning(
                self, "Model Manager", "model_registry layer not found"
            )
            return

        self.layer = layers[0]

        self.layer.dataProvider().forceReload()
        self.layer.triggerRepaint()

        self.model = QStandardItemModel(self)
        self.model.setHorizontalHeaderLabels([
            "Model Name",
            "Layer Name",
            "Tags",
            "Note",
        ])

        self.table.setModel(self.model)
        self.apply_filter()
        self.table.resizeColumnsToContents()

    def apply_filter(self):
        text = self.search.text().lower().strip()

        self.model.removeRows(0, self.model.rowCount())
        self.rows.clear()

        if not self.layer:
            return

        for f in self.layer.getFeatures():
            haystack = " ".join([
                str(f["model_name"] or ""),
                str(f["layer_name"] or ""),
                str(f["tags"] or ""),
                str(f["note"] or ""),
            ]).lower()

            if text and text not in haystack:
                continue

            model_path = f["model_path"]
            exists = self.check_model_exists(model_path)

            items = [
                QStandardItem(str(f["model_name"])),
                QStandardItem(str(f["layer_name"])),
                QStandardItem(str(f["tags"])),
                QStandardItem(str(f["note"])),
            ]

            if not exists:
                for it in items:
                    it.setBackground(QColor("#c0392b"))
                    it.setForeground(QColor("white"))

            self.model.appendRow(items)
            self.rows.append((f, exists))

    def on_double_click(self, index):
        row = index.row()
        feature, exists = self.rows[row]

        if not exists:
            QMessageBox.critical(
                self,
                "Model Not Found",
                f"{feature['model_path']} does not exist in Processing"
            )
            return

        dlg = MemoConfirmDialog(feature["note"], self)
        if dlg.exec_() == QDialog.Accepted:
            processing.execAlgorithmDialog(feature["model_path"])

    def check_model_exists(self, model_path):
        if not model_path:
            return False
        try:
            processing.algorithmHelp(model_path)
            return True
        except Exception:
            return False
