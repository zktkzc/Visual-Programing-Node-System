'''
QGraphicsView的子类，是scene的容器
'''

from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QGraphicsView

import scene


class View(QGraphicsView):
    def __init__(self, scene: scene.Scene, parent=None):
        super().__init__(parent)
        self._scene = scene
        self.setScene(self._scene)
        self.setRenderHints(
            QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        # 隐藏滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # 缩放
        self._zoom_clamp = [0.5, 5]
        self._zoom_factor = 1.05
        self._view_scale = 1.0
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            zoom_factor = self._zoom_factor
        else:
            zoom_factor = 1 / self._zoom_factor
        self._view_scale *= zoom_factor
        if self._view_scale < self._zoom_clamp[0] or self._view_scale > self._zoom_clamp[1]:
            zoom_factor = 1.0
            self._view_scale = self._last_scale

        self._last_scale = self._view_scale
        # 每一次相对于上一次进行缩放
        self.scale(zoom_factor, zoom_factor)
