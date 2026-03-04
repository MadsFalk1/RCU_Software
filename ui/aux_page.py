from __future__ import annotations

from PyQt6.QtWidgets import QCheckBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, QWidget


class AuxPage(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)

        soft = QGroupBox("Soft Start Settings")
        soft_grid = QGridLayout(soft)
        rows = ["HF-1", "LF-2", "HF-4", "LF-3"]
        soft_grid.addWidget(QLabel("Channel"), 0, 0)
        soft_grid.addWidget(QLabel("Enable"), 0, 1)
        soft_grid.addWidget(QLabel("Rate"), 0, 2)
        for i, row in enumerate(rows, start=1):
            soft_grid.addWidget(QLabel(row), i, 0)
            soft_grid.addWidget(QCheckBox(), i, 1)
            soft_grid.addWidget(QLineEdit("0"), i, 2)

        hammer = QGroupBox("Hammer Function")
        hammer_form = QFormLayout(hammer)
        hammer_form.addRow("Valve enable selection", QLineEdit("HF-1"))
        for key in ["Interval A", "A On", "A Off", "Interval B", "B On", "B Off"]:
            hammer_form.addRow(key, QLineEdit("0"))
        hammer_form.addRow("Hammer Enable", QCheckBox())

        turn = QGroupBox("Turn Limit")
        turn_l = QHBoxLayout(turn)
        turn_l.addWidget(QCheckBox("Enable"))
        turn_l.addWidget(QLabel("Limit Value"))
        turn_l.addWidget(QLineEdit("2500"))

        layout.addWidget(soft)
        layout.addWidget(hammer)
        layout.addWidget(turn)
        layout.addStretch(1)
