from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QWidget


class VerticalBarWidget(QWidget):
    def __init__(self, minimum: float = 0.0, maximum: float = 100.0, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.minimum = minimum
        self.maximum = maximum
        self.value = minimum
        self.setMinimumSize(36, 140)

    def set_value(self, value: float) -> None:
        self.value = max(self.minimum, min(self.maximum, value))
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        _ = event
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect().adjusted(6, 6, -6, -6)
        p.setBrush(QColor("#223046"))
        p.setPen(QColor("#9aa8be"))
        p.drawRoundedRect(rect, 8, 8)

        ratio = (self.value - self.minimum) / (self.maximum - self.minimum or 1)
        fill_h = int((rect.height() - 8) * ratio)
        fill_rect = rect.adjusted(4, rect.height() - 4 - fill_h, -4, -4)
        p.setBrush(QColor("#f5922b"))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(fill_rect, 6, 6)
