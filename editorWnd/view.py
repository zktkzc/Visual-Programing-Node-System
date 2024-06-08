"""
QGraphicsView的子类，是scene的容器
"""
from __future__ import annotations

import json
from typing import TYPE_CHECKING, Union, List, Tuple, Dict, Any, Type

import PySide6.QtWidgets
from PySide6.QtCore import Qt, QEvent, QPoint, QPointF
from PySide6.QtGui import QPainter, QMouseEvent
from PySide6.QtWidgets import QGraphicsView, QApplication, QGraphicsProxyWidget, QGraphicsItem

from editorWnd.edge import NodeEdge, DraggingEdge, CuttingLine
from editorWnd.env import ENV
from editorWnd.node import GraphicNode, Node
from editorWnd.node_port import NodePort
from editorWnd.nodes.ActionNode import BeginNode
from editorWnd.widgets import NodeListWidget

if TYPE_CHECKING:
    from editorWnd.scene import Scene


class View(QGraphicsView):
    def __init__(self, scene: Scene, parent=None):
        super().__init__(parent)
        self._scene: Scene = scene
        self._scene.set_view(self)
        self._nodes: List[Union[GraphicNode, Node]] = []
        self._edges: List[NodeEdge] = []
        self.setScene(self._scene)
        self._session_id: int = 0
        self.setRenderHints(
            QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        # 隐藏滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # 缩放
        self._zoom_clamp: List[float] = [0.5, 5]
        self._zoom_factor: float = 1.05
        self._last_scale: float = 1
        self._view_scale: float = 1.0
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)  # 将画布拖动模式设置为橡皮筋模式，即可以拖动框选多个节点
        # 画布拖动
        self._drag_mode: bool = False

        # 可拖动的连接线
        self._dragging_edge: Union[DraggingEdge, None] = None
        self._drag_edge_mode: bool = False

        # 添加cutting line
        self._cutting_mode: bool = False
        self._cutting_line = CuttingLine()
        self._scene.addItem(self._cutting_line)

        # 添加节点选择列表
        self.node_list_widget: Union[NodeListWidget, None] = None
        self.__setup_node_list_widget()
        self._pos_show_node_list_widget: Union[QPoint, QPointF] = QPoint(0, 0)
        # 是否有开始运行节点
        self.__has_begin_node: bool = False
        self._begin_node: Union[BeginNode, None] = None
        # 当前graph保存的路径
        self._saved_path: str = ''

    def get_nodes(self) -> List[Union[GraphicNode, Node]]:
        return self._nodes

    def set_saved_path(self, filepath: str):
        self._saved_path = filepath

    def get_saved_path(self) -> str:
        return self._saved_path

    def save_directly(self) -> bool:
        """
        直接保存当前graph
        :return:
        """
        path = self.get_saved_path()
        if path == '':
            return False
        self.save_graph(path)
        return True

    def __setup_node_list_widget(self):
        # 获取data
        data = ENV.get_nodelib_json_data()
        self.node_list_widget = NodeListWidget(data)
        proxy = self._scene.addWidget(self.node_list_widget)
        proxy.setZValue(2)
        self.node_list_widget.setGeometry(0, 0, 200, 300)
        self.__hide_node_list_widget()
        self.node_list_widget.itemDoubleClicked.connect(self.__node_selected)

    def __node_selected(self, item: PySide6.QtWidgets.QTreeWidgetItem, column):
        if item.data(0, Qt.ItemDataRole.UserRole) is not None:
            node = item.data(0, Qt.ItemDataRole.UserRole)()
            self.add_node(node, (self._pos_show_node_list_widget.x(), self._pos_show_node_list_widget.y()))
            self.__hide_node_list_widget()

    def __show_node_list_widget_at_pos(self, pos: Union[QPoint, QPointF]):
        self.node_list_widget.setGeometry(pos.x(), pos.y(), 200, 300)
        self.node_list_widget.collapseAll()  # 默认折叠所有节点
        self.node_list_widget.show()
        self._pos_show_node_list_widget = pos

    def __hide_node_list_widget(self):
        self.node_list_widget.setVisible(False)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete or event.key() == Qt.Key.Key_X:
            self.__delete_selected_items()
        elif event.key() == Qt.Key.Key_R and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.__run_graph()
        elif event.key() == Qt.Key.Key_S and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.save_graph()
        elif event.key() == Qt.Key.Key_F and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.load_graph()
        super().keyPressEvent(event)

    def save_graph(self, filepath: str = 'graph.json'):
        data: Dict[str, Any] = {'graph_name': '', 'time': '', 'nodes': [], 'edges': []}
        # node
        for node in self._nodes:
            data['nodes'].append(node.to_string())
        # edge
        for edge in self._edges:
            data['edges'].append(edge.to_string())
        json_str = json.dumps(data)
        with open(filepath, 'w') as f:
            f.write(json_str)
        self.set_saved_path(filepath)
        print('视图: 数据保存成功 ->', filepath)

    def __clear_graph(self):
        self._session_id = 0
        for node in self._nodes.copy():
            node.remove_self()
        for edge in self._edges.copy():
            edge.remove_self()
        self._nodes = []
        self._edges = []
        self._scene.update()
        self.update()

    def load_graph(self, filepath: str = 'graph.json'):
        if filepath == self.get_saved_path():
            return
        self.__clear_graph()
        with open(filepath, 'r') as f:
            data = json.loads(f.read())
        nodes = data['nodes']
        edges = data['edges']
        node_id_obj: Dict[int, Union[GraphicNode, Node]] = {}
        for node in nodes:
            # 获取节点类
            cls = ENV.get_cls_by_name(node['class'])
            # 创建节点并添加节点对象
            node_obj = self.__add_node_with_cls(cls, node['pos'])
            node_id = int(node['id'])
            node_id_obj[node_id] = node_obj
            # 设置节点id
            node_obj.set_node_id(node_id)
            # 设置widget的值
            port_value = node['port_values']
            for index, value in port_value.items():
                port = node_obj.get_input_port(int(index))
                port.set_widget_value(value)

        for edge in edges:
            source_node = node_id_obj[edge['source_node_id']]
            dest_node = node_id_obj[edge['dest_node_id']]
            source_port = source_node.get_output_port(edge['source_port_index'])
            dest_port = dest_node.get_input_port(edge['dest_port_index'])
            self.add_node_edge(source_port, dest_port)
        self.set_saved_path(filepath)

        print('视图: 数据加载成功 ->', filepath)

    def __add_node_with_cls(self, cls: Type[Union[GraphicNode, Node]], pos: Tuple[float, float]) -> Union[
        GraphicNode, Node]:
        node = cls()
        self.add_node(node, pos)
        return node

    def __run_graph(self):
        # 找到开始运行节点，如果没有则提示
        if not self.__has_begin_node:
            print('视图: 需要一个【开始运行】节点来运行')
            return
        self.new_session()
        # 找到开始运行节点并开始运行
        self._begin_node.run_node()

    def new_session(self):
        self._session_id += 1
        # 刷新所有节点的状态
        for node in self._nodes:
            node.new_session(self._session_id)

    def stringfy_items(self, items: List[QGraphicsItem]) -> Dict[str, List[Dict[str, Any]]]:
        """
        将选中的节点和边转换为json字符串
        :return:
        """
        data = {
            'edges': [],
            'nodes': [],
            'base_point': None
        }
        for item in items:
            if isinstance(item, Node):
                data['nodes'].append(item.to_string())
                pos = item.scenePos()
                base_point = data['base_point']
                if base_point is None:
                    data['base_point'] = [pos.x(), pos.y()]
                else:
                    if pos.x() < base_point[0]:
                        data['base_point'] = [pos.x(), pos.y()]
            if isinstance(item, NodeEdge):
                data['edges'].append(item.to_string())
        return data

    def itemfy_json_string(self, data: Dict[str, List[Dict[str, Any]]],
                           mouse_position: Union[QPoint, QPointF] = QPointF(0, 0)):
        nodes = data['nodes']
        edges = data['edges']
        base_point = QPointF(data['base_point'][0], data['base_point'][1])
        distance = QPointF(mouse_position.x() - base_point.x(), mouse_position.y() - base_point.y())
        node_id_obj: Dict[int, Union[GraphicNode, Node]] = {}
        for node in nodes:
            # 获取节点类
            cls = ENV.get_cls_by_name(node['class'])
            # 创建节点并添加节点对象
            node_obj = self.__add_node_with_cls(cls, (node['pos'][0] + distance.x(), node['pos'][1] + distance.y()))
            node_obj.setSelected(True)
            node_id = int(node['id'])
            node_id_obj[node_id] = node_obj
            # 设置widget的值

            port_value = node['port_values']
            for index, value in port_value.items():
                port = node_obj.get_input_port(int(index))
                port.set_widget_value(value)

        for edge in edges:
            source_node = node_id_obj.get(edge['source_node_id'], None)
            dest_node = node_id_obj.get(edge['dest_node_id'], None)
            if source_node is None or dest_node is None or source_node.node_title == '开始运行':
                continue
            source_port = source_node.get_output_port(edge['source_port_index'])
            dest_port = dest_node.get_input_port(edge['dest_port_index'])
            edge = self.add_node_edge(source_port, dest_port)
            edge.setSelected(True)

    def unselected_selected_items(self):
        selected_items = self.get_selected_items()
        if len(selected_items) > 0:
            for item in selected_items:
                item.setSelected(False)

    def delete_selected_items(self):
        for item in self.get_selected_items():
            if isinstance(item, Node):
                if item.node_title == '开始运行':
                    self.__has_begin_node = False
                item.remove_self()

    def get_selected_items(self):
        return self._scene.selectedItems()

    def __delete_selected_items(self):
        # 获得当前选中的items
        selected_items = self.get_selected_items()
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
        elif not isinstance(item, QGraphicsProxyWidget):
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
        item = self.itemAt(event.pos())
        if isinstance(item, NodePort):
            if not item.hide_icon:
                QApplication.setOverrideCursor(Qt.CursorShape.PointingHandCursor)
        else:
            if not self._cutting_mode:
                QApplication.setOverrideCursor(Qt.CursorShape.ArrowCursor)
        if self._drag_edge_mode:
            cur_pos = self.mapToScene(event.pos())
            self._dragging_edge.update_position((cur_pos.x(), cur_pos.y()))
        elif self._cutting_mode:
            QApplication.setOverrideCursor(Qt.CursorShape.CrossCursor)
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
        self._cutting_line.clear_points()
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
        """
        鼠标中间点击
        :param event:
        :return:
        """
        if self.itemAt(event.pos()) is not None:
            return
        else:
            # 松开鼠标左键
            release_event = QMouseEvent(QEvent.Type.MouseButtonRelease, event.localPos(), Qt.MouseButton.LeftButton,
                                        Qt.MouseButton.NoButton, event.modifiers())
            super().mouseReleaseEvent(release_event)
            # 改变鼠标样式为小手
            QApplication.setOverrideCursor(Qt.CursorShape.ClosedHandCursor)
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
        QApplication.setOverrideCursor(Qt.CursorShape.ArrowCursor)

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

    def add_node(self, node: GraphicNode, pos: Tuple[float, float] = (0, 0)):
        """
        添加节点
        :return:
        """
        if isinstance(node, BeginNode):
            if self.__has_begin_node:
                print('视图: 添加节点失败，【开始运行】节点已经存在了')
                return
            self.__has_begin_node = True
            self._begin_node = node
        node.setPos(pos[0], pos[1])
        node.set_scene(self._scene)
        self._scene.addItem(node)
        self._nodes.append(node)

    def add_node_edge(self, src_port: NodePort = None, dest_port: NodePort = None) -> NodeEdge:
        edge = NodeEdge(self._scene, src_port, dest_port)
        self._edges.append(edge)
        return edge

    def readd_edge(self, edge: NodeEdge):
        edge.add_to_scene()
        self._edges.append(edge)
        self._scene.update()

    def remove_edge(self, edge: NodeEdge):
        if edge in self._edges:
            self._edges.remove(edge)

    def remove_node(self, node: GraphicNode):
        if node in self._nodes:
            if isinstance(node, BeginNode):
                self.__has_begin_node = False
                self._begin_node = None
            self._nodes.remove(node)
