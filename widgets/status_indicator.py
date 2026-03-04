from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QWidget


class LedIndicator(QWidget):
    def __init__(self, label: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._on = False
        self.label = QLabel(label)
        self.dot = _LedDot()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.dot)
        layout.addWidget(self.label)
        layout.addStretch(1)

    def set_on(self, state: bool) -> None:
        self._on = state
        self.dot.set_on(state)


class _LedDot(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._on = False
        self.setFixedSize(16, 16)

    def set_on(self, state: bool) -> None:
        self._on = state
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        _ = event
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        color = QColor("#44dd55") if self._on else QColor("#556070")
        painter.setBrush(color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(1, 1, self.width() - 2, self.height() - 2)
