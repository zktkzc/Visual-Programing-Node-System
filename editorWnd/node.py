'''
QGraphicsItem的子类
'''
from __future__ import annotations

import abc
from typing import TYPE_CHECKING

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QPen, QColor, QBrush, QPainterPath, QFont
from PySide6.QtWidgets import QGraphicsItem, QGraphicsTextItem, QGraphicsDropShadowEffect

from config import EditorConfig
from node_port import NodePort, ExecInPort, ExecOutPort, ParamPort, OutputPort, NodeOutput, NodeInput

if TYPE_CHECKING:
    from edge import NodeEdge
    from scene import Scene


class GraphicNode(QGraphicsItem):
    def __init__(self, title: str = '', param_ports: list[ParamPort] = None, output_ports: list[OutputPort] = None,
                 is_pure: bool = True, scene: Scene = None, parent=None, node_position: tuple[float, float] = (0, 0),
                 edges: list[NodeEdge] = None, connected_nodes: list[GraphicNode] = None):
        super().__init__(parent)
        self._scene: Scene = scene
        self._node_position: tuple[float, float] = node_position
        self.edges: list[NodeEdge] = edges if edges is not None else []
        self._connected_nodes: list[GraphicNode] = connected_nodes if connected_nodes is not None else []
        self._exec_in: ExecInPort | None = None
        self._exec_out: ExecOutPort | None = None
        # 定义node的大小
        self._min_node_width: float = 20
        self._min_node_height: float = 40
        self._node_width: float = self._min_node_width
        self._node_height: float = self._min_node_height
        self._node_radius: float = 10
        # 左右两个端口之间的间距
        self._port_space: float = 50
        # node的边框
        self._pen_default = QPen(QColor('#151515'))
        self._pen_selected = QPen(QColor('#aaffee00'))
        # node的背景
        self._background_brush = QBrush(QColor('#aa151515'))
        # 节点的标题
        self._title = title
        # 标题的属性
        self._title_height: float = 35
        self._title_font_size: int = EditorConfig.EDITOR_NODE_TITLE_FONT_SIZE
        self._title_font = QFont(EditorConfig.EDITOR_NODE_TITLE_FONT, self._title_font_size)
        self._title_color = Qt.GlobalColor.white
        self._title_padding: float = 5
        self._title_background_brush = QBrush(QColor('#aa00003f'))
        # port的边距
        self._port_padding: float = 7
        self._param_ports: list[ParamPort] = param_ports
        self._output_ports: list[OutputPort] = output_ports
        self._max_param_port_width: float = 0
        self._max_output_port_width: float = 0
        # 选中阴影
        self._shadow = QGraphicsDropShadowEffect()
        self._shadow.setOffset(0, 0)
        self._shadow.setBlurRadius(20)

        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable
            | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
            | QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
        )
        self.__init_title()

        # exec端口
        if is_pure:
            self.__init_node_size()
        else:
            self._node_height += 20
            self.__init_node_size()

        self.__init_ports()

    def __init_ports(self):
        self.__init_param_ports()
        self.__init_output_ports()

    def remove_self(self):
        '''
        删除自己
        :return:
        '''
        # 删除连接边
        for edge in self.edges.copy():
            edge.remove_self()
        # 删除自己
        self._scene.removeItem(self)
        self._scene.get_view().remove_node(self)

    def add_connected_node(self, node: GraphicNode, edge: NodeEdge):
        '''
        添加连接的节点
        :param node:
        :param edge:
        :return:
        '''
        self._connected_nodes.append(node)
        self.edges.append(edge)

    def remove_connected_edge(self, node: GraphicNode, edge: NodeEdge):
        self._connected_nodes.remove(node)
        self.edges.remove(edge)

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            # 更新连接的边
            if len(self.edges) > 0:
                for edge in self.edges:
                    edge.update()
        return super().itemChange(change, value)

    def __init_exec_ports(self):
        self._exec_in = ExecInPort()
        self._exec_out = ExecOutPort()
        self.add_port(self._exec_in)
        self.add_port(self._exec_out)

    def __init_param_ports(self):
        for i, port in enumerate(self._param_ports):
            self.add_port(port, index=i)

    def __init_output_ports(self):
        for i, port in enumerate(self._output_ports):
            self.add_port(port, index=i)

    def __init_node_size(self):
        param_height = len(self._param_ports) * (self._param_ports[0].port_icon_size + self._port_padding)
        for i, port in enumerate(self._param_ports):
            if self._max_param_port_width < port.port_width:
                self._max_param_port_width = port.port_width
        output_height = len(self._output_ports) * (self._output_ports[0].port_icon_size + self._port_padding)
        self._node_height += max(output_height, param_height)
        for i, port in enumerate(self._output_ports):
            if self._max_output_port_width < port.port_width:
                self._max_output_port_width = port.port_width
        if self._max_param_port_width + self._max_output_port_width + self._port_space > self._node_width:
            self._node_width = self._max_param_port_width + self._max_output_port_width + self._port_space

    def set_scene(self, scene: Scene = None):
        self._scene = scene

    def __init_title(self):
        self._title_item = QGraphicsTextItem(self)
        self._title_item.setPlainText(self._title)
        self._title_item.setFont(self._title_font)
        self._title_item.setDefaultTextColor(self._title_color)
        self._title_item.setPos(self._title_padding, 0)

        title_width = self._title_font_size * len(self._title)
        if self._node_width < title_width:
            self._node_width += title_width

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self._node_width, self._node_height)

    def paint(self, painter, option, widget=...) -> None:
        # 先画选中时的阴影
        if self.isSelected():
            self._shadow.setColor(QColor('#cceeee00'))
            self.setGraphicsEffect(self._shadow)
        else:
            self._shadow.setColor(QColor('#00000000'))
            self.setGraphicsEffect(self._shadow)

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
            self._shadow.setColor(Qt.GlobalColor.yellow)
            self.setGraphicsEffect(self._shadow)
        else:
            painter.setPen(self._pen_default)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(node_outline)
            self._shadow.setColor(QColor('#00000000'))
            self.setGraphicsEffect(self._shadow)

    def add_port(self, port: NodePort = None, index: int = 0):
        if port.port_type == NodePort.PORT_TYPE_EXEC_IN:
            self.add_exec_in_port(port, index=index)
        elif port.port_type == NodePort.PORT_TYPE_EXEC_OUT:
            self.add_exec_out_port(port, index=index)
        elif port.port_type == NodePort.PORT_TYPE_PARAM:
            self.add_param_port(port, index=index)
        elif port.port_type == NodePort.PORT_TYPE_OUTPUT:
            self.add_output_param(port, index=index)

    def add_exec_in_port(self, port: NodePort = None, index: int = 0):
        port.setPos(self._port_padding,
                    self._title_height + index * (port.port_icon_size + self._port_padding) + self._port_padding)
        port.add_to_parent_node(parent_node=self, scene=self._scene)

    def add_exec_out_port(self, port: NodePort = None, index: int = 0):
        port.setPos(self._node_width - self._port_padding - port.port_width,
                    self._title_height + index * (port.port_icon_size + self._port_padding) + self._port_padding)
        port.add_to_parent_node(parent_node=self, scene=self._scene)

    def add_param_port(self, port: NodePort = None, index: int = 0):
        port.setPos(self._port_padding,
                    self._title_height + index * (port.port_icon_size + self._port_padding) + self._port_padding)
        port.add_to_parent_node(parent_node=self, scene=self._scene)

    def add_output_param(self, port: NodePort = None, index: int = 0):
        port.setPos(self._node_width - port.port_width - self._port_padding,
                    self._title_height + index * (port.port_icon_size + self._port_padding) + self._port_padding)
        port.add_to_parent_node(parent_node=self, scene=self._scene)


class Node(GraphicNode):
    node_title: str = ''
    node_description: str = ''
    input_pins: list[NodeInput] = []
    output_pins: list[NodeOutput] = []

    def __init__(self):
        # 状态
        self._input_data_ready: bool = False
        self._output_data_ready: bool = False

        self.is_validate()

        in_ports: list[ParamPort] = [pin.init_port() for pin in self.input_pins]
        out_ports: list[OutputPort] = [pin.init_port() for pin in self.output_pins]
        super().__init__(title=self.node_title, param_ports=in_ports, output_ports=out_ports, is_pure=True)

    @abc.abstractmethod
    def run_node(self):
        pass

    def is_validate(self) -> bool:
        if self.node_title == '':
            print('Node: node title could not be empty')
            return False
        if self.node_title is None:
            print('Node: node title could not be None')
            return False
        if self.input_pins is None:
            print('Node: input pins could not be None')
            return False
        if len(self.input_pins) == 0:
            print('Node: input pins could not be empty')
            return False
        if self.output_pins is None:
            self.output_pins = []
        return True

    def input(self, index: int):
        '''
        通过index获取pin中存储的值，如果pin的值为空，需要从与该port相关联的port中来取值
        :param index:
        :return:
        '''
        pass

    def output(self, index: int):
        '''
        设置输出值，并传递给下一个相连的节点的port
        :param index:
        :return:
        '''
        pass

    def exec_output(self, index: int):
        '''
        执行端口
        :param index:
        :return:
        '''
        pass
