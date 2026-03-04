from __future__ import annotations

import math

from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QColor, QFont, QPainter, QPen, QPolygon
from PyQt6.QtWidgets import QWidget


class AnalogGaugeWidget(QWidget):
    def __init__(self, title: str = "", minimum: float = 0.0, maximum: float = 100.0, units: str = "", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.title = title
        self.minimum = minimum
        self.maximum = maximum
        self.units = units
        self.value = minimum
        self.setMinimumSize(220, 220)

    def set_value(self, value: float) -> None:
        self.value = max(self.minimum, min(self.maximum, value))
        self.update()

    def set_range(self, minimum: float, maximum: float) -> None:
        self.minimum = minimum
        self.maximum = maximum
        self.value = max(self.minimum, min(self.maximum, self.value))
        self.update()

    def set_units(self, text: str) -> None:
        self.units = text
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        _ = event
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        side = min(self.width(), self.height())
        p.translate(self.width() / 2, self.height() / 2)
        p.scale(side / 240.0, side / 240.0)

        self._draw_background(p)
        self._draw_ticks(p)
        self._draw_needle(p)
        self._draw_labels(p)

    def _draw_background(self, p: QPainter) -> None:
        p.setBrush(QColor("#1e2d44"))
        p.setPen(QPen(QColor("#aeb8c6"), 2))
        p.drawEllipse(-110, -110, 220, 220)

    def _draw_ticks(self, p: QPainter) -> None:
        p.save()
        p.setPen(QPen(QColor("#d6dde6"), 2))
        for i in range(11):
            angle = -210 + i * 24
            rad = math.radians(angle)
            p.drawLine(int(84 * math.cos(rad)), int(84 * math.sin(rad)), int(102 * math.cos(rad)), int(102 * math.sin(rad)))
        p.restore()

    def _draw_needle(self, p: QPainter) -> None:
        span = self.maximum - self.minimum or 1.0
        ratio = (self.value - self.minimum) / span
        angle_deg = -210 + ratio * 240
        p.save()
        p.rotate(angle_deg)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor("#f5922b"))
        poly = QPolygon([QPoint(-6, 0), QPoint(0, -6), QPoint(84, 0), QPoint(0, 6)])
        p.drawPolygon(poly)
        p.restore()

        p.setBrush(QColor("#dfe5ed"))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(-8, -8, 16, 16)

    def _draw_labels(self, p: QPainter) -> None:
        p.setPen(QColor("#ffffff"))
        p.setFont(QFont("Arial", 9, QFont.Weight.Bold))
        p.drawText(-104, -120, 208, 20, Qt.AlignmentFlag.AlignCenter, self.title)
        p.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        p.drawText(-80, 18, 160, 24, Qt.AlignmentFlag.AlignCenter, f"{self.value:.1f}")
        p.setFont(QFont("Arial", 8))
        p.drawText(-80, 38, 160, 20, Qt.AlignmentFlag.AlignCenter, self.units)
