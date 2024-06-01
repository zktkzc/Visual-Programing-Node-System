'''
QGraphicsView的子类，是scene的容器
'''
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QPainter, QMouseEvent
from PySide6.QtWidgets import QGraphicsView

from edge import NodeEdge, DraggingEdge
from node import Node
from node_port import NodePort

if TYPE_CHECKING:
    from scene import Scene


class View(QGraphicsView):
    def __init__(self, scene: Scene, parent=None):
        super().__init__(parent)
        self._scene = scene
        self._scene.set_view(self)
        self._nodes: list[Node] = []
        self._edges: list[NodeEdge] = []
        self.setScene(self._scene)
        self.setRenderHints(
            QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        # 隐藏滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # 缩放
        self._zoom_clamp: list[float] = [0.5, 5]
        self._zoom_factor: float = 1.05
        self._view_scale: float = 1.0
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)  # 将画布拖动模式设置为橡皮筋模式，即可以拖动框选多个节点
        # 画布拖动
        self._drag_mode: bool = False

        # 可拖动的连接线
        self._dragging_edge: DraggingEdge | None = None
        self._drag_edge_mode: bool = False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete or event.key() == Qt.Key.Key_X:
            self.delete_selected_items()

    def delete_selected_items(self):
        # 获得当前选中的items
        selected_items = self._scene.selectedItems()
        for item in selected_items:
            if isinstance(item, Node):
                item.remove_self()
            elif isinstance(item, NodeEdge):
                item.remove_self()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            # 鼠标中间点击
            self.__middle_button_pressed(event)
        elif event.button() == Qt.MouseButton.LeftButton:
            # 鼠标左键点击
            self.__left_button_pressed(event)
        else:
            super().mousePressEvent(event)

    def __left_button_pressed(self, event):
        mouse_pos = event.pos()
        item = self.itemAt(mouse_pos)
        if isinstance(item, NodePort):
            # 是端口
            self._drag_edge_mode = True
            self.__create_dragging_edge(item)
        else:
            super().mousePressEvent(event)

    def __create_dragging_edge(self, port: NodePort) -> None:
        port_pos = port.get_port_pos()
        if port.port_type == NodePort.PORT_TYPE_EXEC_OUT or port.port_type == NodePort.PORT_TYPE_OUTPUT:
            drag_from_src = True
        else:
            drag_from_src = False

        if self._dragging_edge is None:
            self._dragging_edge = DraggingEdge(src_pos=(port_pos.x(), port_pos.y()),
                                               dst_pos=(port_pos.x(), port_pos.y()),
                                               drag_from_src=drag_from_src, scene=self._scene,
                                               edge_color=port.port_color)
            self._dragging_edge.set_first_port(port)
            self._scene.addItem(self._dragging_edge)

    def mouseMoveEvent(self, event):
        if self._drag_edge_mode:
            cur_pos = self.mapToScene(event.pos())
            self._dragging_edge.update_position((cur_pos.x(), cur_pos.y()))
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.__middle_button_released(event)
        elif event.button() == Qt.MouseButton.LeftButton:
            self.__left_button_released(event)
        else:
            super().mouseReleaseEvent(event)

    def __left_button_released(self, event):
        if self._drag_edge_mode:
            self._drag_edge_mode = False
            item = self.itemAt(event.pos())
            if isinstance(item, NodePort):
                self._dragging_edge.set_second_port(item)
                # 创建一个连接线
                edge = self._dragging_edge.create_node_edge()
                if edge is not None:
                    self._edges.append(edge)
            # 删除当前连接线
            self._scene.removeItem(self._dragging_edge)
            self._dragging_edge = None
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.__reset_scale()
        else:
            super().mouseDoubleClickEvent(event)

    def __middle_button_pressed(self, event):
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

    def __middle_button_released(self, event):
        release_event = QMouseEvent(QEvent.Type.MouseButtonRelease, event.localPos(), Qt.MouseButton.LeftButton,
                                    Qt.MouseButton.NoButton, event.modifiers())
        super().mouseReleaseEvent(release_event)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
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

    def __reset_scale(self):
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
        self._nodes.append(node)

    def add_node_edge(self, src_port: NodePort = None, dest_port: NodePort = None):
        edge = NodeEdge(self._scene, src_port, dest_port)
        self._edges.append(edge)

    def remove_edge(self, edge: NodeEdge):
        if edge in self._edges:
            self._edges.remove(edge)

    def remove_node(self, node: Node):
        if node in self._nodes:
            self._nodes.remove(node)
