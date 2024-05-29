'''
节点的连接边
'''
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPen, QPainterPath, QPainter, QColor
from PySide6.QtWidgets import QGraphicsItem, QGraphicsPathItem, QGraphicsDropShadowEffect

from node_port import NodePort
from scene import Scene


class NodeEdge(QGraphicsPathItem):
    def __init__(self, scene: Scene = None, src_port: NodePort = None, dest_port: NodePort = None,
                 edge_color: str = '#ffffff', parent=None):
        super().__init__(parent)

        self._src_port = src_port
        self._dest_port = dest_port
        self._scene = scene
        # 初始画笔
        self._edge_color = self._src_port.port_color if edge_color == '#ffffff' else edge_color
        self._default_pen = QPen(QColor(self._edge_color))
        self._default_pen.setWidthF(2)
        # 选中投影
        self._shadow = QGraphicsDropShadowEffect()
        self._shadow.setOffset(0, 0)
        self._shadow.setBlurRadius(20)
        self._shadow_color = Qt.GlobalColor.yellow
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setZValue(-1)  # 降低线的级别

        self.add_to_scene()

    def add_to_scene(self):
        self._scene.addItem(self)
        # 相关节点的port更新内容
        self._src_port.add_edge(self, self._dest_port)
        self._dest_port.add_edge(self, self._src_port)

    def update_edge_path(self):
        '''
        更新路径
        :return:
        '''
        src_pos = self._src_port.get_port_pos()
        dest_pos = self._dest_port.get_port_pos()
        path = QPainterPath(src_pos)
        # 计算贝塞尔曲线手柄的长度
        x_width = abs(src_pos.x() - dest_pos.x()) + 1
        y_height = abs(src_pos.y() - dest_pos.y())
        tangent = float(y_height) / x_width * 0.5
        tangent = tangent if tangent < 1 else 1
        tangent *= x_width
        path.cubicTo(QPointF(src_pos.x() + tangent, src_pos.y()), QPointF(dest_pos.x() - tangent, dest_pos.y()),
                     dest_pos)
        self.setPath(path)

    def paint(self, painter: QPainter, option, widget=...):
        # 画线
        self.update_edge_path()
        painter.setPen(self._default_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(self.path())

        if self.isSelected():
            self._shadow.setColor(self._shadow_color)
            self.setGraphicsEffect(self._shadow)
        else:
            self._shadow.setColor('#00000000')
            self.setGraphicsEffect(self._shadow)


class DraggingEdge(QGraphicsPathItem):
    def __init__(self, parent=None, src_pos: tuple[float, float] = (0, 0), dst_pos: tuple[float, float] = (0, 0),
                 edge_color: str = '#ffffff', scene: Scene = None, drag_from_src: bool = True):
        super().__init__(parent)
        self._src_pos: tuple[float, float] = src_pos
        self._dst_pos: tuple[float, float] = dst_pos
        self._scene: Scene = scene
        self._edge_color: str = edge_color
        self._drag_from_src: bool = drag_from_src
        self.src_port: NodePort | None = None
        self.dst_port: NodePort | None = None
        # 初始画笔
        self._default_pen = QPen(QColor(self._edge_color))
        self._default_pen.setWidthF(2)
        self.setZValue(-1)

    def paint(self, painter, option, widget=...):
        self.update_edge_path()
        painter.setPen(self._default_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(self.path())

    def update_edge_path(self):
        '''
        更新连接边的路径
        :return:
        '''
        src_pos: QPointF = QPointF(self._src_pos[0], self._src_pos[1])
        dest_pos: QPointF = QPointF(self._dst_pos[0], self._dst_pos[1])
        path = QPainterPath(src_pos)
        # 计算贝塞尔曲线手柄的长度
        x_width = abs(src_pos.x() - dest_pos.x()) + 1
        y_height = abs(src_pos.y() - dest_pos.y())
        tangent = float(y_height) / x_width * 0.5
        tangent = tangent if tangent < 1 else 1
        tangent *= x_width
        path.cubicTo(QPointF(src_pos.x() + tangent, src_pos.y()), QPointF(dest_pos.x() - tangent, dest_pos.y()),
                     dest_pos)
        self.setPath(path)

    def update_position(self, pos: tuple[float, float] = (0, 0)):
        if self._drag_from_src:
            self._dst_pos = pos
        else:
            self._src_pos = pos
        self.update()

    def set_first_port(self, port: NodePort):
        if self._drag_from_src:
            self.src_port = port
        else:
            self.dst_port = port

    def set_second_port(self, port: NodePort):
        if not self._drag_from_src:
            self.src_port = port
        else:
            self.dst_port = port

    def create_node_edge(self):
        if self.__can_connect():
            NodeEdge(scene=self._scene, src_port=self.src_port, dest_port=self.dst_port, edge_color=self._edge_color)
            self.src_port.fill()
            self.dst_port.fill()

    def __is_pair(self) -> bool:
        if self.src_port.port_type == NodePort.PORT_TYPE_EXEC_OUT and self.dst_port.port_type == NodePort.PORT_TYPE_EXEC_IN:
            return True
        elif self.src_port.port_type == NodePort.PORT_TYPE_OUTPUT and self.dst_port.port_type == NodePort.PORT_TYPE_PARAM:
            return True
        return False

    def __not_in_same_node(self):
        if self.src_port.parent_node == self.dst_port.parent_node:
            return False
        return True

    def __has_same_class(self):
        if self.src_port.port_class == self.dst_port.port_class:
            return True
        return False

    def __can_connect(self) -> bool:
        '''
        判断两个端口是否能够连接
        :param port1:
        :param port2:
        :return:
        '''
        if self.__is_pair() and self.__has_same_class() and self.__not_in_same_node():
            return True
        return False
