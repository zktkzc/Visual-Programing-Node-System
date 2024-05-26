'''
编辑器主体
'''
from __future__ import annotations

from PySide6.QtWidgets import QWidget, QBoxLayout

from node import Node
from node_port import ExecInPort, ExecOutPort, ParamPort, OutputPort
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

    def debug_add_node(self):
        param_ports: list[ParamPort] = []
        param_ports.append(ParamPort('宽度', 'float', '#99ff22'))
        param_ports.append(ParamPort('高度', 'float', '#99ff22'))

        output_params: list[OutputPort] = []
        output_params.append(OutputPort('面积', 'float', '#99ff22'))

        node = Node(title='面积', param_ports=param_ports, output_ports=output_params, is_pure=False)
        self.view.add_node(node, (0, 0))
