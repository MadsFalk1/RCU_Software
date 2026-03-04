from __future__ import annotations

from PyQt6.QtWidgets import QFormLayout, QGroupBox, QLineEdit, QVBoxLayout, QWidget


class LogSetupPage(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)

        test_meta = QGroupBox("Test Metadata")
        form1 = QFormLayout(test_meta)
        form1.addRow("Test Title", QLineEdit('P-test cement plug inside 20" casing to 75 bar'))
        form1.addRow("Operator", QLineEdit("Shell"))
        form1.addRow("Rig", QLineEdit("West Navigator"))

        logging = QGroupBox("Logging Parameters")
        form2 = QFormLayout(logging)
        form2.addRow("Log Time [min]", QLineEdit("10"))
        form2.addRow("Log Time [turn]", QLineEdit("2"))

        graph_scale = QGroupBox("Graph Scale")
        form3 = QFormLayout(graph_scale)
        form3.addRow("Y-scale Min", QLineEdit("-3000"))
        form3.addRow("Y-scale Max", QLineEdit("3000"))

        layout.addWidget(test_meta)
        layout.addWidget(logging)
        layout.addWidget(graph_scale)
        layout.addStretch(1)
