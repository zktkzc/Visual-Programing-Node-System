"""
Node Port的实现
"""
from __future__ import annotations

import abc
import string
from typing import TYPE_CHECKING, Any, Type, List, Union

from PySide6.QtCore import Qt, QRectF, QPointF, QPoint
from PySide6.QtGui import QPainterPath, QColor, QBrush, QFont, QPolygonF, QPen, QIntValidator, QDoubleValidator
from PySide6.QtWidgets import QGraphicsItem, QGraphicsProxyWidget, QLineEdit, QCheckBox

from editorWnd.config import NodeConfig, EditorConfig
from editorWnd.dtypes import DTypes

if TYPE_CHECKING:
    from editorWnd.scene import Scene
    from editorWnd.node import GraphicNode, Node
    from editorWnd.edge import NodeEdge


class NodePort(QGraphicsItem):
    PORT_TYPE_EXEC_IN = 1001
    PORT_TYPE_EXEC_OUT = 1002
    PORT_TYPE_PARAM = 1003
    PORT_TYPE_OUTPUT = 1004

    def __init__(self, port_label: str = '', port_class: str = 'str', port_color: str = '#ffffff',
                 port_type: int = PORT_TYPE_EXEC_IN, parent=None, connected_ports: list[NodePort] = None,
                 edges: list[NodeEdge] = None, default_widget: Type | None = None, hide_icon: bool = False):
        super().__init__(parent)

        self._edges: List[NodeEdge] = edges if edges is not None else []
        self._connected_ports: list[NodePort] = connected_ports if connected_ports is not None else []
        self._port_label: str = port_label
        self.hide_icon: bool = hide_icon
        self._scene: Union[Scene, None] = None
        self.port_class = port_class
        self.port_color: str = port_color
        self.port_type: int = port_type
        self._port_font_size: int = EditorConfig.EDITOR_NODE_PIN_LABEL_FONT_SIZE
        self._port_font: QFont = QFont(EditorConfig.EDITOR_NODE_PIN_LABEL_FONT, self._port_font_size)
        self.port_icon_size: float = NodeConfig.PORT_ICON_SIZE
        self.port_label_size: int = (len(self._port_label) + self.__get_chinese_count(
            self._port_label)) * self._port_font_size
        self.port_width: float = self.port_icon_size + self.port_label_size

        self.parent_node: Union[GraphicNode, Node, None] = None
        self._port_pos: Union[QPointF, QPoint] = QPointF(0, 0)

        self._session_id: int = 0

        # 定义pen和brush
        self._default_pen: QPen = QPen(QColor(self.port_color))
        self._default_pen.setWidthF(1.5)
        self._default_brush: QBrush = QBrush(QColor(self.port_color))

        self._default_widget: Union[Type[QLineEdit], Type[QCheckBox], None] = None
        if default_widget:
            self._default_widget = default_widget()
        if isinstance(self._default_widget, QLineEdit):
            self._default_widget.setTextMargins(0, 0, 0, 0)
            self._default_widget.setFixedWidth(30)
            self._default_widget.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            self._default_widget.setStyleSheet(
                '''
                background-color: transparent;
                border: 1px solid #9499b3;
                color: #9499b3;
                '''
            )
            self.port_width += 25
        elif isinstance(self._default_widget, QCheckBox):
            self._default_widget.setFixedSize(20, 20)
            self._default_widget.setStyleSheet(
                '''
                QCheckBox::indicator {
                    width: 20px;
                    height: 20px;
                }
                QCheckBox {
                    background-color: transparent;
                }
                '''
            )
            self.port_width += 25

        # port中存储的值
        self._port_value: Any = None
        self._has_set_value: bool = False

        self._port_index:int = 0

    def new_session(self, session_id: int):
        self._session_id = session_id
        self._has_set_value = False
        self._port_value = None

    def is_connected(self) -> bool:
        return len(self._edges) > 0

    def has_set_value(self) -> bool:
        return self._has_set_value

    def set_port_value(self, value: Union[str, int, float, bool, None]):
        self._has_set_value = True
        self._port_value = value

    def get_port_value(self) -> Union[str, int, float, bool, None]:
        return self._port_value

    def get_default_value(self) -> Union[str, bool, int, float, None]:
        if self._default_widget is None or not self._default_widget.isVisible():
            self._port_value = None
            self._has_set_value = False
            return None
        else:
            if isinstance(self._default_widget, QLineEdit):
                if self.port_class == DTypes.Integer:
                    try:
                        self._port_value = int(self._default_widget.text())
                    except:
                        pass
                elif self.port_class == DTypes.Float:
                    try:
                        self._port_value = float(self._default_widget.text())
                    except:
                        pass
                else:
                    self._port_value = self._default_widget.text()
                return self._port_value
            elif isinstance(self._default_widget, QCheckBox):
                self._port_value = self._default_widget.isChecked()
                return self._port_value

    def set_widget_value(self, value: Any):
        if isinstance(self._default_widget, QLineEdit):
            self._default_widget.setText(str(value))
        elif isinstance(self._default_widget, QCheckBox):
            self._default_widget.setChecked(value)

    def get_value_from_connected_port(self) -> Union[str, int, float, bool, None]:
        if self.is_connected():
            connected_port = self._connected_ports[0]
            # 如果连接的端口没有设置值，强制执行parent_node
            if not connected_port._has_set_value:
                connected_port.parent_node.run_node()
            return connected_port._port_value
        else:
            print(f'节点: {self.parent_node.node_title}的{self._port_label}端口还没有设置值且没有连接的边')
            return None

    def get_connected_ports(self) -> List[NodePort]:
        """
        获取与当前端口连接的端口
        :return: 端口列表
        """
        return self._connected_ports

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

    def add_edge(self, edge: NodeEdge, port: NodePort):
        self.__remove_edge_by_condition()
        self.parent_node.add_connected_node(port.parent_node, edge)
        self._edges.append(edge)
        self._connected_ports.append(port)

    def __remove_edge_by_condition(self):
        if self.port_type == NodePort.PORT_TYPE_EXEC_IN or self.port_type == NodePort.PORT_TYPE_PARAM or self.port_type == NodePort.PORT_TYPE_EXEC_OUT:
            # 将已有的连接线删除
            if len(self._edges) > 0:
                for edge in self._edges:
                    edge.remove_self()

    def remove_edge(self, edge: NodeEdge):
        if edge not in self._edges:
            return
        self._edges.remove(edge)
        if edge.src_port == self:
            self._connected_ports.remove(edge.dest_port)
            self.parent_node.remove_connected_edge(edge.dest_port.parent_node, edge)
        else:
            self._connected_ports.remove(edge.src_port)
            self.parent_node.remove_connected_edge(edge.src_port.parent_node, edge)

    @abc.abstractmethod
    def _fill_port(self, painter):
        pass

    def get_port_pos(self) -> Union[QPointF, None]:
        if self.hide_icon:
            return None
        # 获得本身在scene内的位置
        self._port_pos = self.scenePos()
        return QPointF(self._port_pos.x() + 0.25 * self.port_icon_size, self._port_pos.y() + 0.5 * self.port_icon_size)

    def boundingRect(self):
        return QRectF(0, 0, self.port_width, self._port_font_size)

    def add_to_parent_node(self, parent_node: GraphicNode = None, scene: Scene = None):
        self.setParentItem(parent_node)
        self.parent_node = parent_node
        self._scene = scene

    def set_port_index(self, index: int):
        self._port_index = index

    def get_port_index(self) -> int:
        return self._port_index


class ExecPort(NodePort):
    def __init__(self, port_label: str = '', port_class: str = 'str', port_color: str = '#ffffff',
                 port_type: int = NodePort.PORT_TYPE_EXEC_IN, parent=None):
        super().__init__(port_label, port_class, port_color, port_type, parent)

    def _fill_port(self, painter):
        pass

    def paint(self, painter, option, widget=...):
        pass


class ExecInPort(ExecPort):
    def __init__(self, port_label: str = ''):
        super().__init__(port_type=NodePort.PORT_TYPE_EXEC_IN, port_label=port_label)

    def _fill_port(self, painter):
        port_outline = QPainterPath()
        poly = QPolygonF()
        poly.append(QPointF(1.8, 0.3 * self.port_icon_size))
        poly.append(QPointF(0.2 * self.port_icon_size, 0.3 * self.port_icon_size))
        poly.append(QPointF(0.38 * self.port_icon_size, 0.5 * self.port_icon_size))
        poly.append(QPointF(0.2 * self.port_icon_size, 0.7 * self.port_icon_size))
        poly.append(QPointF(1.8, 0.7 * self.port_icon_size))
        port_outline.addPolygon(poly)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(self.port_color)))
        painter.drawPath(port_outline.simplified())

    def paint(self, painter, option, widget=...):
        port_outline = QPainterPath()
        poly = QPolygonF()
        poly.append(QPointF(0, 0.2 * self.port_icon_size))
        poly.append(QPointF(0.25 * self.port_icon_size, 0.2 * self.port_icon_size))
        poly.append(QPointF(0.5 * self.port_icon_size, 0.5 * self.port_icon_size))
        poly.append(QPointF(0.25 * self.port_icon_size, 0.8 * self.port_icon_size))
        poly.append(QPointF(0, 0.8 * self.port_icon_size))
        port_outline.addPolygon(poly)
        painter.setPen(self._default_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(port_outline.simplified())

        if len(self._edges) > 0:
            self._fill_port(painter)

        painter.setPen(self._default_pen)
        painter.setFont(self._port_font)
        painter.drawText(
            QRectF(self.port_icon_size, 0, self.port_label_size, self.port_icon_size),
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self._port_label)


class ExecOutPort(ExecPort):
    def __init__(self, port_label: str = ''):
        super().__init__(port_type=NodePort.PORT_TYPE_EXEC_OUT, port_label=port_label)

    def _fill_port(self, painter):
        port_outline = QPainterPath()
        poly = QPolygonF()
        poly.append(QPointF(self.port_label_size + 0.5 * self.port_icon_size + 1.8, 0.3 * self.port_icon_size))
        poly.append(QPointF(self.port_label_size + 0.5 * self.port_icon_size + 0.2 * self.port_icon_size,
                            0.3 * self.port_icon_size))
        poly.append(QPointF(self.port_label_size + 0.5 * self.port_icon_size + 0.38 * self.port_icon_size,
                            0.5 * self.port_icon_size))
        poly.append(QPointF(self.port_label_size + 0.5 * self.port_icon_size + 0.2 * self.port_icon_size,
                            0.7 * self.port_icon_size))
        poly.append(QPointF(self.port_label_size + 0.5 * self.port_icon_size + 1.8, 0.7 * self.port_icon_size))
        port_outline.addPolygon(poly)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(self.port_color)))
        painter.drawPath(port_outline.simplified())

    def paint(self, painter, option, widget=...):
        painter.setPen(self._default_pen)
        painter.setFont(self._port_font)
        painter.drawText(
            QRectF(0, 0, self.port_label_size, self.port_icon_size),
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, self._port_label)

        port_outline = QPainterPath()
        poly = QPolygonF()
        poly.append(QPointF(self.port_label_size + 0.5 * self.port_icon_size, 0.2 * self.port_icon_size))
        poly.append(QPointF(self.port_label_size + 0.5 * self.port_icon_size + 0.25 * self.port_icon_size,
                            0.2 * self.port_icon_size))
        poly.append(QPointF(self.port_label_size + 0.5 * self.port_icon_size + 0.5 * self.port_icon_size,
                            0.5 * self.port_icon_size))
        poly.append(QPointF(self.port_label_size + 0.5 * self.port_icon_size + 0.25 * self.port_icon_size,
                            0.8 * self.port_icon_size))
        poly.append(QPointF(self.port_label_size + 0.5 * self.port_icon_size + 0, 0.8 * self.port_icon_size))
        port_outline.addPolygon(poly)
        painter.setPen(self._default_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(port_outline.simplified())

        if len(self._edges) > 0:
            self._fill_port(painter)

    def get_port_pos(self) -> QPointF:
        # 获得本身在scene内的位置
        port_pos = self.scenePos()
        return QPointF(port_pos.x() + self.port_label_size + 0.75 * self.port_icon_size,
                       port_pos.y() + 0.5 * self.port_icon_size)


class ParamPort(NodePort):
    def __init__(self, port_label: str = '', port_class: str = 'str', port_color: str = '#ffffff', parent=None,
                 default_widget=None, hide_icon=False):
        super().__init__(port_label, port_class, port_color, NodePort.PORT_TYPE_PARAM, parent,
                         default_widget=default_widget, hide_icon=hide_icon)
        self._has_set_value = len(self._edges) > 0
        self.__init_default_widget()

    def _fill_port(self, painter):
        # 填充
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(self.port_color)))
        painter.drawEllipse(QPointF(0.25 * self.port_icon_size, 0.5 * self.port_icon_size),
                            0.15 * self.port_icon_size,
                            0.15 * self.port_icon_size)

    def paint(self, painter, option, widget=...):
        if not self.hide_icon:
            # 圆
            painter.setPen(self._default_pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(QPointF(0.25 * self.port_icon_size, 0.5 * self.port_icon_size),
                                0.25 * self.port_icon_size, 0.25 * self.port_icon_size)

            # 三角
            poly = QPolygonF()
            poly.append(QPointF(0.6 * self.port_icon_size, 0.35 * self.port_icon_size))
            poly.append(QPointF(0.75 * self.port_icon_size, 0.5 * self.port_icon_size))
            poly.append(QPointF(0.6 * self.port_icon_size, 0.65 * self.port_icon_size))
            painter.setBrush(self._default_brush)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawPolygon(poly)

            # 文字
            painter.setPen(self._default_pen)
            painter.setFont(self._port_font)
            painter.drawText(
                QRectF(self.port_icon_size, 0, self.port_label_size, self.port_icon_size),
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self._port_label)

        if len(self._edges) > 0:
            self._fill_port(painter)
            if self._default_widget:
                self._default_widget.setVisible(False)
        else:
            if self._default_widget:
                self._default_widget.setVisible(True)

    def __init_default_widget(self):
        # 得到参数的类型
        if self.port_class == DTypes.Integer:
            self._default_widget.setValidator(QIntValidator())
        elif self.port_class == DTypes.Float:
            self._default_widget.setValidator(QDoubleValidator())
        proxy = QGraphicsProxyWidget(self)
        proxy.setWidget(self._default_widget)
        if self.hide_icon:
            proxy.setPos(10, 0)
        else:
            proxy.setPos(self.port_icon_size + self.port_label_size, 0)


class OutputPort(NodePort):
    def __init__(self, port_label: str = '', port_class: str = 'str', port_color: str = '#ffffff', parent=None):
        super().__init__(port_label, port_class, port_color, NodePort.PORT_TYPE_OUTPUT, parent)

    def _fill_port(self, painter):
        # 填充
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(self.port_color)))
        painter.drawEllipse(
            QPointF(self.port_label_size + 0.5 * self.port_icon_size, 0.5 * self.port_icon_size),
            0.15 * self.port_icon_size,
            0.15 * self.port_icon_size)

    def get_port_pos(self) -> QPointF:
        # 获得本身在scene内的位置
        port_pos = self.scenePos()
        return QPointF(port_pos.x() + self.port_label_size + 0.5 * self.port_icon_size,
                       port_pos.y() + 0.5 * self.port_icon_size)

    def paint(self, painter, option, widget=...):
        # 文字
        painter.setPen(self._default_pen)
        painter.setFont(self._port_font)
        painter.drawText(
            QRectF(0, 0, self.port_label_size, self.port_icon_size),
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, self._port_label)

        # 圆
        painter.setPen(self._default_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(QPointF(self.port_label_size + 0.5 * self.port_icon_size, 0.5 * self.port_icon_size),
                            0.25 * self.port_icon_size,
                            0.25 * self.port_icon_size)

        if len(self._edges) > 0:
            self._fill_port(painter)

        # 三角
        poly = QPolygonF()
        poly.append(QPointF(self.port_label_size + 0.85 * self.port_icon_size, 0.35 * self.port_icon_size))
        poly.append(QPointF(self.port_label_size + 1.00 * self.port_icon_size, 0.5 * self.port_icon_size))
        poly.append(QPointF(self.port_label_size + 0.85 * self.port_icon_size, 0.65 * self.port_icon_size))
        painter.setBrush(self._default_brush)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPolygon(poly)


class Pin:
    class PinType:
        DATA = 'data'
        EXEC = 'exec'

    def __init__(self, pin_name: str = '', pin_class: str = '', use_default_widget: bool = True, pin_type: PinType = '',
                 pin_widget=None, hide_icon: bool = False):
        self._pin_name = pin_name
        self.pin_type = pin_type
        if self.pin_type == Pin.PinType.DATA:
            self.pin_class = pin_class
            self._pin_color = DTypes.Color_Map[pin_class]
            if use_default_widget:
                self._pin_widget = DTypes.default_widget.get(pin_class, None)
            else:
                self._pin_widget = pin_widget
        self.port: Union[NodePort, None] = None
        self._hide_icon: bool = hide_icon

    def get_pin_type(self) -> PinType:
        return self.pin_type

    @abc.abstractmethod
    def init_port(self, index: int):
        pass


class NodeInput(Pin):
    def init_port(self, index) -> ParamPort:
        if self.pin_type == Pin.PinType.DATA:
            self.port = ParamPort(port_label=self._pin_name, port_class=self.pin_class, port_color=self._pin_color,
                                  default_widget=self._pin_widget, hide_icon=self._hide_icon)
            self.port.set_port_index(index)
        elif self.pin_type == Pin.PinType.EXEC:
            self.port = ExecInPort(port_label=self._pin_name)
            self.port.set_port_index(index)
        else:
            self.port = None
            print('no such kinds of pin type')
        return self.port


class NodeOutput(Pin):
    def init_port(self, index) -> OutputPort:
        if self.pin_type == Pin.PinType.DATA:
            self.port = OutputPort(port_label=self._pin_name, port_class=self.pin_class, port_color=self._pin_color)
            self.port.set_port_index(index)
        elif self.pin_type == Pin.PinType.EXEC:
            self.port = ExecOutPort(port_label=self._pin_name)
            self.port.set_port_index(index)
        else:
            self.port = None
            print('no such kinds of pin type')
        return self.port
