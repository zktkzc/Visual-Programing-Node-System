'''
QGraphicsView的子类，是scene的容器
'''
from __future__ import annotations

from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QPainter, QMouseEvent
from PySide6.QtWidgets import QGraphicsView

from node import Node
from scene import Scene


class View(QGraphicsView):
    def __init__(self, scene: Scene, parent=None):
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
        # 画布拖动
        self._drag_mode = False

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.middle_button_pressed(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.middle_button_released(event)
        else:
            super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.reset_scale()
        else:
            super().mouseDoubleClickEvent(event)

    def middle_button_pressed(self, event):
        '''
        鼠标中间点击
        :param event:
        :return:
        '''
        if self.itemAt(event.pos()) is not None:
            return
        else:
            # 松开鼠标左键
            release_event = QMouseEvent(QEvent.Type.MouseButtonRelease, event.localPos(), Qt.MouseButton.LeftButton,
                                        Qt.MouseButton.NoButton, event.modifiers())
            super().mouseReleaseEvent(release_event)
            # 改变鼠标样式为小手
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
            self._drag_mode = True
            # 默认为鼠标左键拖动，现在需要同时按住鼠标中建让图标变为小手，太麻烦了，因此创建手动创建一个鼠标左键点击的事件
            click_event = QMouseEvent(QEvent.Type.MouseButtonPress, event.localPos(), Qt.MouseButton.LeftButton,
                                      Qt.MouseButton.NoButton, event.modifiers())
            super().mousePressEvent(click_event)

    def middle_button_released(self, event):
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self._drag_mode = False

    def wheelEvent(self, event):
        if not self._drag_mode:
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

    def reset_scale(self):
        self.resetTransform()
        self._view_scale = 1.0

    def add_node(self, node: Node, pos: tuple[float, float] = (0, 0)):
        '''
        添加节点
        :return:
        '''
        node.setPos(pos[0], pos[1])
        node.set_scene(self._scene)
        self._scene.addItem(node)

