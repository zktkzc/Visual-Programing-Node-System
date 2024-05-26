'''
Node Port的实现
'''
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QPainterPath, QColor, QBrush, QFont, QPolygonF, QPen
from PySide6.QtWidgets import QGraphicsItem

from scene import Scene

if TYPE_CHECKING:
    from node import Node


class NodePort(QGraphicsItem):
    PORT_TYPE_EXEC_IN = 1001
    PORT_TYPE_EXEC_OUT = 1002
    PORT_TYPE_PARAM = 1003
    PORT_TYPE_OUTPUT = 1004

    def __init__(self, port_label: str = '', port_class: str = 'str', port_color: str = '#ffffff',
                 port_type: int = PORT_TYPE_EXEC_IN, parent=None):
        super().__init__(parent)

        self._port_label = port_label
        self._port_class = port_class
        self._port_color = port_color
        self.port_type = port_type
        self._port_font_size = 12
        self._port_font = QFont('微软雅黑', self._port_font_size)
        self.port_icon_size = 20
        self._port_label_size = len(self._port_label) * self._port_font_size
        self.port_width = self.port_icon_size + self._port_label_size

        # 定义pen和brush
        self._default_pen = QPen(QColor(self._port_color))
        self._default_pen.setWidthF(1.5)
        self._default_brush = QBrush(QColor(self._port_color))

    def boundingRect(self):
        return QRectF(0, 0, self.port_width, self._port_font_size)

    def add_to_parent_node(self, parent_node: Node = None, scene: Scene = None):
        self.setParentItem(parent_node)
        self._parent_node = parent_node
        self._scene = scene


class ExecPort(NodePort):
    def __init__(self, port_label: str = '', port_class: str = 'str', port_color: str = '#ffffff',
                 port_type: int = NodePort.PORT_TYPE_EXEC_IN, parent=None):
        super().__init__(port_label, port_class, port_color, port_type, parent)

    def paint(self, painter, option, widget=...):
        port_outline = QPainterPath()
        poly = QPolygonF()
        poly.append(QPointF(0, 0.2 * self.port_icon_size))
        poly.append(QPointF(0.25 * self.port_icon_size, 0.2 * self.port_icon_size))
        poly.append(QPointF(0.5 * self.port_icon_size, 0.5 * self.port_icon_size))
        poly.append(QPointF(0.25 * self.port_icon_size, 0.8 * self.port_icon_size))
        poly.append(QPointF(0, 0.8 * self.port_icon_size))
        port_outline.addPolygon(poly)
        painter.setPen(self._default_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(port_outline.simplified())


class ExecInPort(ExecPort):
    def __init__(self):
        super().__init__(port_type=NodePort.PORT_TYPE_EXEC_IN)


class ExecOutPort(ExecPort):
    def __init__(self):
        super().__init__(port_type=NodePort.PORT_TYPE_EXEC_OUT)
