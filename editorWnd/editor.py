'''
编辑器主体
'''
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QBoxLayout

from editorWnd.env import ENV
from editorWnd.node import GraphicNode
from editorWnd.node_port import ParamPort, OutputPort
from editorWnd.scene import Scene
from editorWnd.view import View


class Editor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        ENV.init_node_env()
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
        # self.debug_add_node()
        self.show()

    def debug_add_node(self, pos: tuple[float, float] = (0, 0)):
        param_ports: list[ParamPort] = []
        param_ports.append(ParamPort('宽度', 'float', '#99ff22'))
        param_ports.append(ParamPort('高度', 'float', '#99ff22'))
        param_ports.append(ParamPort('计数', 'int', '#00ffee'))

        output_params: list[OutputPort] = []
        output_params.append(OutputPort('面积', 'float', '#99ff22'))
        output_params.append(OutputPort('数量', 'int', '#00ffee'))

        node = GraphicNode(title='面积', param_ports=param_ports, output_ports=output_params, is_pure=False)
        self.view.add_node(node, pos)

    def debug_add_custom_node(self, pos: tuple[float, float] = (0, 0)):
        node = ENV.get_registered_node_cls()[1]()
        self.view.add_node(node, pos)

    def right_click_add_node(self, mouse_pos):
        '''
        右键添加节点
        :param mouse_pos: 鼠标点击的位置
        :return:
        '''
        self.debug_add_custom_node((mouse_pos.x(), mouse_pos.y()))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            # self.right_click_add_node(self.view.mapToScene(event.pos()))  # 将鼠标位置从屏幕映射到scene中的位置
            pass
        else:
            super().mousePressEvent(event)
