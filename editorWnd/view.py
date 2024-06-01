'''
QGraphicsView的子类，是scene的容器
'''
from __future__ import annotations

from typing import TYPE_CHECKING

import PySide6.QtWidgets
from PySide6.QtCore import Qt, QEvent, QPoint, QPointF
from PySide6.QtGui import QPainter, QMouseEvent
from PySide6.QtWidgets import QGraphicsView, QApplication

from edge import NodeEdge, DraggingEdge, CuttingLine
from env import ENV
from node import GraphicNode
from node_port import NodePort
from widgets import NodeListWidget

if TYPE_CHECKING:
    from scene import Scene


class View(QGraphicsView):
    def __init__(self, scene: Scene, parent=None):
        super().__init__(parent)
        self._scene = scene
        self._scene.set_view(self)
        self._nodes: list[GraphicNode] = []
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

        # 添加cutting line
        self._cutting_mode: bool = False
        self._cutting_line = CuttingLine()
        self._scene.addItem(self._cutting_line)

        # 添加节点选择列表
        self.node_list_widget: NodeListWidget | None = None
        self.__setup_node_list_widget()
        self._pos_show_node_list_widget: QPoint | QPointF = QPoint(0, 0)

    def __setup_node_list_widget(self):
        # 获取data
        data = ENV.get_nodelib_json_data()
        self.node_list_widget = NodeListWidget(data)
        self._scene.addWidget(self.node_list_widget)
        self.node_list_widget.setGeometry(0, 0, 200, 300)
        self.__hide_node_list_widget()
        self.node_list_widget.itemDoubleClicked.connect(self.__node_selected)

    def __node_selected(self, item: PySide6.QtWidgets.QTreeWidgetItem, column):
        if item.data(0, Qt.ItemDataRole.UserRole) is not None:
            node = item.data(0, Qt.ItemDataRole.UserRole)()
            self.add_node(node, (self._pos_show_node_list_widget.x(), self._pos_show_node_list_widget.y()))
            self.__hide_node_list_widget()

    def __show_node_list_widget_at_pos(self, pos: QPoint | QPointF):
        self.node_list_widget.setGeometry(pos.x(), pos.y(), 200, 300)
        self.node_list_widget.show()
        self._pos_show_node_list_widget = pos

    def __hide_node_list_widget(self):
        self.node_list_widget.setVisible(False)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete or event.key() == Qt.Key.Key_X:
            self.__delete_selected_items()

    def __delete_selected_items(self):
        # 获得当前选中的items
        selected_items = self._scene.selectedItems()
        for item in selected_items:
            if isinstance(item, GraphicNode):
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
        elif event.button() == Qt.MouseButton.RightButton:
            self.__right_button_pressed_process(event)
        else:
            super().mousePressEvent(event)

    def __right_button_pressed_process(self, event):
        item = self.itemAt(event.pos())
        if item is None:
            if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                self._cutting_mode = True
                QApplication.setOverrideCursor(Qt.CursorShape.CrossCursor)  # 设置鼠标样式为十字架状
            else:
                # 右键显示节点列表
                self.__show_node_list_widget_at_pos(self.mapToScene(event.pos()))
        else:
            self.setDragMode(QGraphicsView.DragMode.NoDrag)
        super().mousePressEvent(event)

    def __left_button_pressed(self, event):
        mouse_pos = event.pos()
        item = self.itemAt(mouse_pos)
        if isinstance(item, NodePort):
            # 是端口
            self._drag_edge_mode = True
            self.__create_dragging_edge(item)
        elif item is None:
            self.__hide_node_list_widget()
            super().mousePressEvent(event)
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
        elif self._cutting_mode:
            self._cutting_line.update_points(self.mapToScene(event.pos()))
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.__middle_button_released(event)
        elif event.button() == Qt.MouseButton.LeftButton:
            self.__left_button_released(event)
        elif event.button() == Qt.MouseButton.RightButton:
            self.__right_button_released_process(event)
        else:
            super().mouseReleaseEvent(event)

    def __right_button_released_process(self, event):
        # 获得和cutting line相交的边，并删除
        self._cutting_line.remove_intersect_edges(self._edges)
        # 清除cutting line
        self._cutting_mode = False
        self._cutting_line.line_points.clear()
        self._cutting_line.update()
        QApplication.setOverrideCursor(Qt.CursorShape.ArrowCursor)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

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

    def add_node(self, node: GraphicNode, pos: tuple[float, float] = (0, 0)):
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

    def remove_node(self, node: GraphicNode):
        if node in self._nodes:
            self._nodes.remove(node)
