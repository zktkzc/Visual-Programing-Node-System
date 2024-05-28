'''
节点的连接边
'''
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPen, QPainterPath, QPainter
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
        self._edge_color = self._src_port.port_color
        self._default_pen = QPen(self._edge_color)
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
