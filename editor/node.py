'''
QGraphicsItem的子类
'''
from PySide6.QtWidgets import QGraphicsItem, QGraphicsTextItem
from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QPainter, QPen, QColor, QBrush, QPainterPath, QFont
from config import EditorConfig


class Node(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 定义node的大小
        self._node_width: float = 240
        self._node_height: float = 160
        self._node_radius: float = 10
        # node的边框
        self._pen_default = QPen(QColor('#151515'))
        self._pen_selected = QPen(QColor('#aaffee00'))
        # node的背景
        self._background_brush = QBrush(QColor('#aa151515'))

        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsMovable|QGraphicsTextItem.GraphicsItemFlag.ItemIsSelectable)

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self._node_width, self._node_height)

    def paint(self, painter, option, widget=...) -> None:
        # 画背景颜色
        node_outline = QPainterPath()
        node_outline.addRoundedRect(0, 0, self._node_width, self._node_height, self._node_radius, self._node_radius)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._background_brush)
        painter.drawPath(node_outline.simplified())

        if self.isSelected():
            painter.setPen(self._pen_selected)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(node_outline)
        else:
            painter.setPen(self._pen_default)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(node_outline)
