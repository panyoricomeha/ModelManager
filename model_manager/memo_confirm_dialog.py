# -*- coding: utf-8 -*-

from qgis.PyQt.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QTextEdit,
    QDialogButtonBox
)


class MemoConfirmDialog(QDialog):
    """
    Confirmation dialog shown before executing a model.
    Displays the memo content in read-only mode.
    """

    def __init__(self, memo_text, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Confirm Execution")
        self.resize(400, 250)

        layout = QVBoxLayout(self)

        text = QTextEdit()
        text.setReadOnly(True)
        text.setText(memo_text or "")
        layout.addWidget(text)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)
