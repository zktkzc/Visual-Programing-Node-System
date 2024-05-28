'''
编辑器主体
'''
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QBoxLayout

from node import Node
from node_port import ParamPort, OutputPort
from scene import Scene
from view import View


class Editor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_editor()

    def setup_editor(self):
        # 窗口位置以及大小
        self.setGeometry(100, 100, 1200, 700)
        self.setWindowTitle('可视化编程编辑器')
        self.layout = QBoxLayout(QBoxLayout.Direction.LeftToRight, self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # 初始化scene
        self.scene = Scene()
        self.view = View(self.scene, self)
        self.layout.addWidget(self.view)
        self.debug_add_node()
        self.show()

    def debug_add_node(self, pos: tuple[float, float] = (0, 0)):
        param_ports: list[ParamPort] = []
        param_ports.append(ParamPort('宽度', 'float', '#99ff22'))
        param_ports.append(ParamPort('高度', 'float', '#99ff22'))

        output_params: list[OutputPort] = []
        output_params.append(OutputPort('面积', 'float', '#99ff22'))

        node = Node(title='面积', param_ports=param_ports, output_ports=output_params, is_pure=False)
        self.view.add_node(node, pos)

        param_ports2: list[ParamPort] = []
        param_ports2.append(ParamPort('宽度', 'float', '#99ff22'))
        param_ports2.append(ParamPort('高度', 'float', '#99ff22'))

        output_params2: list[OutputPort] = []
        output_params2.append(OutputPort('面积', 'float', '#99ff22'))
        node2 = Node(title='面积', param_ports=param_ports2, output_ports=output_params2, is_pure=False)
        self.view.add_node(node2, (pos[0] + 300, pos[1] + 200))

        self.view.add_node_edge(output_params[0], param_ports2[0])

    def right_click_add_node(self, mouse_pos):
        '''
        右键添加节点
        :param mouse_pos: 鼠标点击的位置
        :return:
        '''
        self.debug_add_node((mouse_pos.x(), mouse_pos.y()))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.right_click_add_node(self.view.mapToScene(event.pos()))  # 将鼠标位置从屏幕映射到scene中的位置
        else:
            super().mousePressEvent(event)
