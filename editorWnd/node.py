"""
QGraphicsItem的子类
"""
from __future__ import annotations

import abc
import string
import uuid
from typing import TYPE_CHECKING, Union, List, Any, Dict

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QPen, QColor, QBrush, QPainterPath, QFont
from PySide6.QtWidgets import QGraphicsItem, QGraphicsTextItem, QGraphicsDropShadowEffect

from editorWnd.config import EditorConfig, NodeConfig
from editorWnd.node_port import NodePort, ExecInPort, ExecOutPort, ParamPort, OutputPort, NodeOutput, NodeInput, Pin

if TYPE_CHECKING:
    from editorWnd.group import NodeGroup
    from editorWnd.edge import NodeEdge
    from editorWnd.scene import Scene


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
        self._node_radius: float = NodeConfig.NODE_RADIUS
        # 左右两个端口之间的间距
        self._port_space: float = 50
        # node的边框
        self._pen_default = QPen(QColor('#4e90fe'))
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
        self._title_background_brush = QBrush(QColor('#aa4e90fe'))
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

        # 所属的组
        self._group: Union[NodeGroup, None] = None

    def __init_ports(self):
        self.__init_param_ports()
        self.__init_output_ports()

    def remove_self(self):
        """
        删除自己
        :return:
        """
        # 删除连接边
        for edge in self.edges.copy():
            edge.remove_self()
        # 删除自己
        if self._scene is not None:
            self._scene.removeItem(self)
            self._scene.get_view().remove_node(self)
        self.update()

    def add_connected_node(self, node: GraphicNode, edge: NodeEdge):
        """
        添加连接的节点
        :param node:
        :param edge:
        :return:
        """
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
        param_height = len(self._param_ports) * (NodeConfig.PORT_ICON_SIZE + self._port_padding)
        for i, port in enumerate(self._param_ports):
            if self._max_param_port_width < port.port_width:
                self._max_param_port_width = port.port_width
        output_height = len(self._output_ports) * (NodeConfig.PORT_ICON_SIZE + self._port_padding)
        self._node_height += max(output_height, param_height)
        for i, port in enumerate(self._output_ports):
            if self._max_output_port_width < port.port_width:
                self._max_output_port_width = port.port_width
        if self._max_param_port_width + self._max_output_port_width + self._port_space > self._node_width:
            self._node_width = self._max_param_port_width + self._max_output_port_width + self._port_space

    def set_scene(self, scene: Scene = None):
        self._scene = scene

    def __init_title(self):
        color = QColor(NodeConfig.node_title_background_color.get(self.pkg_name, '#4e90fe'))
        self._pen_default = QPen(color)
        color.setAlphaF(0.6)
        self._title_background_brush = QBrush(color)

        self._title_item = QGraphicsTextItem(self)
        self._title_item.setPlainText(self._title)
        self._title_item.setFont(self._title_font)
        self._title_item.setDefaultTextColor(self._title_color)
        self._title_item.setPos(self._title_padding, 0)

        title_width = self._title_font_size * (len(self._title) + self.__get_chinese_count(self._title))
        if self._node_width < title_width:
            self._node_width += title_width

    def __get_chinese_count(self, s: str) -> int:
        """
        获取字符串中中文字符的数量
        :param s: 字符串
        :return: 中文字符的个数
        """
        __count = 0
        for c in s:
            if c.isalpha() and c not in string.ascii_letters:
                __count += 1
        return __count

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
            self.setZValue(1)
        else:
            painter.setPen(self._pen_default)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(node_outline)
            self._shadow.setColor(QColor('#00000000'))
            self.setGraphicsEffect(self._shadow)
            self.setZValue(0)

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

    # ==========================================  group设置  =========================================================
    def add_to_group(self, group: NodeGroup):
        if self._group is not None and self._group != group:
            self.remove_from_group()
        self._group = group

    def remove_from_group(self):
        self._group.remove_node(self)
        self._group = None


class Node(GraphicNode):
    pkg_name: str = ''
    node_title: str = ''
    node_description: str = ''
    input_pins: List[NodeInput] = []
    output_pins: List[NodeOutput] = []

    def __init__(self):
        # 状态
        self._input_data_ready: bool = False
        self._output_data_ready: bool = False

        self._session_id: int = 0
        self._node_id: int = uuid.uuid1().int

        self.is_validate()

        self.in_ports: List[Union[ParamPort, ExecInPort]] = \
            [self.input_pins[i].init_port(i) for i in range(len(self.input_pins))]
        self.out_ports: List[Union[OutputPort, ExecOutPort]] = \
            [self.output_pins[i].init_port(i) for i in range(len(self.output_pins))]
        super().__init__(title=self.node_title, param_ports=self.in_ports, output_ports=self.out_ports, is_pure=True)

    def set_node_id(self, node_id: int):
        self._node_id = node_id

    def get_node_id(self) -> int:
        return self._node_id

    @abc.abstractmethod
    def run_node(self):
        pass

    def new_session(self, session_id: int):
        """
        创建新的session
        :param session_id:
        :return:
        """
        self._session_id = session_id
        for port in self.in_ports:
            port.new_session(self._session_id)
        for port in self.out_ports:
            port.new_session(self._session_id)

    def is_validate(self) -> bool:
        if self.node_title == '':
            print('节点: 节点标题不能为空')
            return False
        if self.node_title is None:
            print('节点: 节点标题不能为None')
            return False
        if self.input_pins is None:
            print('节点: 输入端口不能为None')
            return False
        if self.output_pins is None:
            self.output_pins = []
        return True

    def input(self, index: int) -> Any:
        """
        通过index获取pin中存储的值，如果pin的值为空，需要从与该port相关联的port中来取值
        :param index: 索引
        :return: pin中存储的值
        """
        pin = self.input_pins[index]
        if not pin.pin_type == Pin.PinType.DATA:
            print(f'节点: {self.node_title}的第{index}个端口不是一个数据端口')
            return None
        port = self.in_ports[index]
        port_value = port.get_default_value()
        if port_value is None:
            # 有连接的节点，从连接的节点获取值
            port_value = port.get_value_from_connected_port()
        return port_value

    def output(self, index: int, value: Any):
        """
        设置输出值，并传递给下一个相连的节点的port
        :param value: 要设置的值
        :param index: 索引
        :return:
        """
        pin = self.output_pins[index]
        if not pin.pin_type == Pin.PinType.DATA:
            print(f'节点: {self.node_title}的第{index}个端口不是一个数据端口')
            return None
        self.out_ports[index].set_port_value(value)

    def exec_input(self, index) -> Union[bool, None]:
        pin = self.input_pins[index]
        if not pin.pin_type == Pin.PinType.EXEC:
            print(f'节点: {self.node_title}的第{index}个端口不是一个执行端口')
            return None
        # 如果是，则获取该端口连接的节点
        port = self.in_ports[index]
        return port.get_port_value()

    def exec_output(self, index: int):
        """
        执行端口
        :param index:
        :return:
        """
        pin = self.output_pins[index]
        if not pin.pin_type == Pin.PinType.EXEC:
            print(f'节点: {self.node_title}的第{index}个端口不是一个执行端口')
            return
        # 如果是，则获取该端口连接的节点
        port = self.out_ports[index]
        connected_ports = port.get_connected_ports()
        for port in connected_ports:
            port.set_port_value(True)
            port.parent_node.run_node()

    def get_input_port(self, index: int) -> Union[ParamPort, ExecInPort]:
        if 0 <= index < len(self.in_ports):
            return self.in_ports[index]

    def get_output_port(self, index: int) -> Union[OutputPort, ExecOutPort]:
        if 0 <= index < len(self.out_ports):
            return self.out_ports[index]

    def to_string(self) -> Dict[str, Any]:
        node: Dict[str, Any] = {
            'id': self._node_id,
            'class': self.__class__.__name__,
            'module': self.__class__.__module__,
            'pos': (self.scenePos().x(), self.scenePos().y()),
            'port_values': {}
        }
        for index, port in enumerate(self.in_ports):
            value = port.get_default_value()
            if value is not None:
                node['port_values'][index] = value
        return node
