'''
QGraphicsItem的子类
'''
from __future__ import annotations

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QPen, QColor, QBrush, QPainterPath, QFont
from PySide6.QtWidgets import QGraphicsItem, QGraphicsTextItem

from node_port import NodePort, ExecInPort, ExecOutPort, ParamPort, OutputPort
from scene import Scene


class Node(QGraphicsItem):
    def __init__(self, title: str = '', param_ports: list[ParamPort] = None, output_ports: list[OutputPort] = None,
                 is_pure: bool = False, scene: Scene = None,
                 parent=None):
        super().__init__(parent)
        self._scene = scene
        self._exec_in: ExecInPort | None = None
        self._exec_out: ExecOutPort | None = None
        # 定义node的大小
        self._min_node_width: float = 20
        self._min_node_height: float = 60
        self._node_width: float = self._min_node_width
        self._node_height: float = self._min_node_height
        self._node_radius: float = 10
        # 左右两个端口之间的间距
        self._port_space: float = 100
        # node的边框
        self._pen_default = QPen(QColor('#151515'))
        self._pen_selected = QPen(QColor('#aaffee00'))
        # node的背景
        self._background_brush = QBrush(QColor('#aa151515'))
        # 节点的标题
        self._title = title
        # 标题的属性
        self._title_height: float = 35
        self._title_font_size: int = 13
        self._title_font = QFont('微软雅黑', self._title_font_size)
        self._title_color = Qt.GlobalColor.white
        self._title_padding: float = 3
        self._title_background_brush = QBrush(QColor('#aa00003f'))
        # port的边距
        self._port_padding: float = 6
        self._port_index: float = 0
        self._param_ports: list[ParamPort] = param_ports
        self._output_ports: list[OutputPort] = output_ports
        self._max_param_port_width: float = 0
        self._max_output_port_width: float = 0

        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable | QGraphicsTextItem.GraphicsItemFlag.ItemIsSelectable)
        self.init_title()

        # exec端口
        if is_pure:
            self._node_height -= 20
            self.init_node_size()
        else:
            self.init_node_size()
            self.init_exec_ports()
            self._port_index = 1

        # param端口
        self.init_param_ports()

        # output端口
        self.init_output_ports()

    def get_exec_in(self) -> ExecInPort:
        return self._exec_in

    def get_exec_out(self) -> ExecOutPort:
        return self._exec_out

    def init_exec_ports(self):
        self._exec_in = ExecInPort()
        self._exec_out = ExecOutPort()
        self.add_port(self._exec_in)
        self.add_port(self._exec_out)

    def init_param_ports(self):
        for i, port in enumerate(self._param_ports):
            self.add_port(port, index=i + self._port_index)

    def init_output_ports(self):
        for i, port in enumerate(self._output_ports):
            self.add_port(port, index=i + self._port_index)

    def init_node_size(self):
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

    def init_title(self):
        self._title_item = QGraphicsTextItem(self)
        self._title_item.setPlainText(self._title)
        self._title_item.setFont(self._title_font)
        self._title_item.setDefaultTextColor(self._title_color)
        self._title_item.setPos(self._title_padding, self._title_padding)

        title_width = self._title_font_size * len(self._title)
        if self._node_width < title_width:
            self._node_width += title_width

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self._node_width, self._node_height)

    def paint(self, painter, option, widget=...) -> None:
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
        else:
            painter.setPen(self._pen_default)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(node_outline)

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
        port.setPos(self._port_padding, self._title_height)
        port.add_to_parent_node(parent_node=self, scene=self._scene)

    def add_exec_out_port(self, port: NodePort = None, index: int = 0):
        port.setPos(self._node_width + 0.5 * port.port_icon_size - self._port_padding - port.port_width,
                    self._title_height)
        port.add_to_parent_node(parent_node=self, scene=self._scene)

    def add_param_port(self, port: NodePort = None, index: int = 0):
        port.setPos(self._port_padding, self._title_height + index * (port.port_icon_size + self._port_padding))
        port.add_to_parent_node(parent_node=self, scene=self._scene)

    def add_output_param(self, port: NodePort = None, index: int = 0):
        port.setPos(self._node_width - port.port_width - self._port_padding,
                    self._title_height + index * (port.port_icon_size + self._port_padding))
        port.add_to_parent_node(parent_node=self, scene=self._scene)
