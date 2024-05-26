'''
编辑器主体
'''
from __future__ import annotations

from PySide6.QtWidgets import QWidget, QBoxLayout

from node import Node
from node_port import ExecInPort, ExecOutPort
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
        exec_in_port = ExecInPort()
        exec_out_port = ExecOutPort()
        node = Node(title='测试')
        node.add_exec_in_port(exec_in_port)
        node.add_exec_out_port(exec_out_port)
        self.view.add_node(node, (0, 0))
