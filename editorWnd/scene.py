'''
QGraphicsScene的子类
'''
from __future__ import annotations

import math
from typing import Union, TYPE_CHECKING

import PySide6.QtGui
from PySide6.QtCore import Qt, QLine
from PySide6.QtGui import QBrush, QColor, QPen
from PySide6.QtWidgets import QGraphicsScene

from editorWnd.config import EditorConfig

if TYPE_CHECKING:
    from editorWnd.view import View


class Scene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._view: View | None = None
        self.setBackgroundBrush(QBrush(QColor('#212121')))
        self._width = EditorConfig.EDITOR_SCENE_WIDTH
        self._height = EditorConfig.EDITOR_SCENE_HEIGHT
        self._grid_size = EditorConfig.EDITOR_SCENE_GRID_SIZE
        self._chunk_size = EditorConfig.EDITOR_SCENE_GRID_CHUNK
        # 设置背景大小
        self.setSceneRect(-self._width / 2, -self._height / 2, self._width, self._height)
        # 画网格
        self._normal_line_pen = QPen(QColor(EditorConfig.EDITOR_SCENE_GRID_NORMAL_LINE_COLOR))
        self._normal_line_pen.setWidthF(EditorConfig.EDITOR_SCENE_GRID_NORMAL_LINE_WIDTH)
        self._dark_line_pen = QPen(QColor(EditorConfig.EDITOR_SCENE_GRID_DARK_LINE_COLOR))
        self._dark_line_pen.setWidthF(EditorConfig.EDITOR_SCENE_GRID_DARK_LINE_WIDTH)

    def set_view(self, view: View):
        self._view = view

    def get_view(self) -> View:
        return self._view

    def drawBackground(self, painter: PySide6.QtGui.QPainter,
                       rect: Union[PySide6.QtCore.QRectF, PySide6.QtCore.QRect]) -> None:
        super().drawBackground(painter, rect)
        lines, dark_lines = self.calc_grid_lines(rect)
        # 画普通的线
        painter.setPen(self._normal_line_pen)
        painter.drawLines(lines)
        # 画框线
        painter.setPen(self._dark_line_pen)
        painter.drawLines(dark_lines)

    def calc_grid_lines(self, rect: Union[PySide6.QtCore.QRectF, PySide6.QtCore.QRect]):
        """
        计算出所有要画的表格线
        :param rect:
        :return:
        """
        left, right, top, bottom = math.floor(rect.left()), math.floor(rect.right()), math.floor(
            rect.top()), math.floor(rect.bottom())
        # 最左边的线
        first_left = left - (left % self._grid_size)
        # 最上边的线
        first_top = top - (top % self._grid_size)

        lines: list = []
        dark_lines: list = []

        # 画横线
        for v in range(first_top, bottom, self._grid_size):
            line = QLine(left, v, right, v)
            if v % (self._grid_size * self._chunk_size) == 0:
                dark_lines.append(line)
            else:
                lines.append(line)

        # 画竖线
        for h in range(first_left, right, self._grid_size):
            line = QLine(h, top, h, bottom)
            if h % (self._grid_size * self._chunk_size) == 0:
                dark_lines.append(line)
            else:
                lines.append(line)

        return lines, dark_lines
