from __future__ import annotations

from typing import TYPE_CHECKING, List

from PySide6.QtCore import QRectF, Qt, QPointF
from PySide6.QtGui import QPen, QColor, QBrush, QFont, QPainterPath
from PySide6.QtWidgets import QGraphicsItem, QGraphicsTextItem

from editorWnd.config import GroupConfig

if TYPE_CHECKING:
    from editorWnd.scene import Scene


class NodeGroup(QGraphicsItem):
    def __init__(self, scene: Scene = None, items: List[QGraphicsItem] = None, group_width: float = 800,
                 group_height: float = 400):
        super().__init__(None)
        self._scene: Scene = scene
        self._items = items
        self._group_title: str = ''

        # ===============================================  标题 ===============================================
        self._group_title_height: float = 40
        self._group_title_padding: float = 5
        self._title_pen = QPen(QColor(GroupConfig.GROUP_TITLE_COLOR))
        self._title_brush_color = QColor(GroupConfig.GROUP_TITLE_BACKGROUND_COLOR)
        self._title_brush_color.setAlphaF(0.8)
        self._title_brush = QBrush(self._title_brush_color)
        self._title_font = QFont(GroupConfig.GROUP_TITLE_FONT, GroupConfig.GROUP_TITLE_FONT_SIZE)
        self._title_item = QGraphicsTextItem(self)
        self._title_item.setPlainText(self._group_title)
        self._title_item.setFont(self._title_font)
        self._title_item.setDefaultTextColor(QColor(GroupConfig.GROUP_TITLE_COLOR))
        self._title_item.setPos(self._group_title_padding, 0)
        # =====================================================================================================

        # =============================================  选中的效果  ============================================
        self._pen_selected = QPen(QColor('#ddffee00'))
        self._pen_selected.setWidth(2)
        # =====================================================================================================

        self._scene.addItem(self)
        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable |
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable
        )
        self.setZValue(-1)

        self._group_padding: float = 20
        self._group_min_width: float = group_width + 2 * self._group_padding
        self._group_min_height: float = group_height + self._group_title_height + self._group_padding * 2
        self._group_pos = QPointF(-self._group_padding, -self._group_title_height - self._group_padding)

    def boundingRect(self):
        return QRectF(self._group_pos.x(), self._group_pos.y(), self._group_min_width, self._group_min_height)

    def paint(self, painter, option, widget=...):
        # ============================================  内容背景  ============================================
        node_outline = QPainterPath()
        node_outline.addRoundedRect(
            self._group_pos.x(), self._group_pos.y(),
            self._group_min_width, self._group_min_height,
            GroupConfig.GROUP_RADIUS, GroupConfig.GROUP_RADIUS
        )
        painter.setPen(Qt.PenStyle.NoPen)
        content_brush_color = QColor(GroupConfig.GROUP_CONTENT_BACKGROUND_COLOR)
        content_brush_color.setAlphaF(0.5)
        painter.setBrush(QBrush(content_brush_color))
        painter.drawPath(node_outline.simplified())
        # ===================================================================================================

        # =============================================  标题背景  ============================================
        title_outline = QPainterPath()
        title_outline.setFillRule(Qt.FillRule.WindingFill)
        title_outline.addRoundedRect(
            self._group_pos.x(), self._group_pos.y(),
            self._group_min_width, self._group_title_height,
            GroupConfig.GROUP_RADIUS, GroupConfig.GROUP_RADIUS
        )
        title_outline.addRect(
            self._group_pos.x(), self._group_pos.y() + self._group_title_height - GroupConfig.GROUP_RADIUS,
            GroupConfig.GROUP_RADIUS, GroupConfig.GROUP_RADIUS
        )
        title_outline.addRect(
            self._group_pos.x() + self._group_min_width - GroupConfig.GROUP_RADIUS,
            self._group_pos.y() + self._group_title_height - GroupConfig.GROUP_RADIUS,
            GroupConfig.GROUP_RADIUS, GroupConfig.GROUP_RADIUS
        )
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._title_brush)
        painter.drawPath(title_outline.simplified())
        # ===================================================================================================

        # =============================================  选中的效果  ==========================================
        if not self.isSelected():
            painter.setPen(QPen(QColor(GroupConfig.GROUP_TITLE_BACKGROUND_COLOR)))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(node_outline.simplified())
        else:
            painter.setPen(self._pen_selected)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(node_outline.simplified())

            if len(self._items) > 0:
                for item in self._items:
                    item.setSelected(True)
        # ===================================================================================================

    def remove_self(self):
        self._scene.removeItem(self)
