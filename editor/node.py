'''
QGraphicsItem的子类
'''
from __future__ import annotations

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QPen, QColor, QBrush, QPainterPath, QFont
from PySide6.QtWidgets import QGraphicsItem, QGraphicsTextItem

from node_port import NodePort
from scene import Scene


class Node(QGraphicsItem):
    def __init__(self, title: str = '', scene: Scene = None, parent=None):
        super().__init__(parent)
        self._scene = scene
        # 定义node的大小
        self._node_width: float = 240
        self._node_height: float = 160
        self._node_radius: float = 10
        # node的边框
        self._pen_default = QPen(QColor('#151515'))
        self._pen_selected = QPen(QColor('#aaffee00'))
        # node的背景
        self._background_brush = QBrush(QColor('#aa151515'))
        # 节点的标题
        self._title = title
        # 标题的属性
        self._title_height = 35
        self._title_font = QFont('微软雅黑', 13)
        self._title_color = Qt.GlobalColor.white
        self._title_padding = 3
        self._title_background_brush = QBrush(QColor('#aa00003f'))
        # port的边距
        self._port_padding = 6

        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable | QGraphicsTextItem.GraphicsItemFlag.ItemIsSelectable)
        self.init_title()

    def init_title(self):
        self._title_item = QGraphicsTextItem(self)
        self._title_item.setPlainText(self._title)
        self._title_item.setFont(self._title_font)
        self._title_item.setDefaultTextColor(self._title_color)
        self._title_item.setPos(self._title_padding, self._title_padding)

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self._node_width, self._node_height)

    def paint(self, painter, option, widget=...) -> None:
        # 画背景颜色
        node_outline = QPainterPath()
        node_outline.addRoundedRect(0, 0, self._node_width, self._node_height, self._node_radius, self._node_radius)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._background_brush)
        painter.drawPath(node_outline.simplified())

        # 画标题的背景
        title_outline = QPainterPath()
        title_outline.setFillRule(Qt.FillRule.WindingFill)
        title_outline.addRoundedRect(0, 0, self._node_width, self._title_height, self._node_radius, self._node_radius)
        # 在左下角和右下角分别画两个矩形盖住倒角
        title_outline.addRect(0, self._title_height - self._node_radius, self._node_radius, self._node_radius)
        title_outline.addRect(self._node_width - self._node_radius, self._title_height - self._node_radius,
                              self._node_radius, self._node_radius)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._title_background_brush)
        painter.drawPath(title_outline.simplified())

        # 先画所有的背景，再画选择时的线，防止线被盖住
        if self.isSelected():
            painter.setPen(self._pen_selected)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(node_outline)
        else:
            painter.setPen(self._pen_default)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(node_outline)

    def add_port(self, port: NodePort = None):
        if port.port_type == NodePort.PORT_TYPE_EXEC_IN:
            self.add_exec_in_port(port)
        elif port.port_type == NodePort.PORT_TYPE_EXEC_OUT:
            self.add_exec_out_port()

    def add_exec_in_port(self, port: NodePort = None):
        port.setPos(self._port_padding, self._title_height)
        port.add_to_parent_node(parent_node=self, scene=self._scene)

    def add_exec_out_port(self, port: NodePort = None):
        port.setPos(self._node_width + 0.5 * port.port_icon_size - self._port_padding - port.port_width, self._title_height)
        port.add_to_parent_node(parent_node=self, scene=self._scene)
