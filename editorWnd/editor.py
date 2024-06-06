"""
编辑器主体
"""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication, QAction
from PySide6.QtWidgets import QWidget, QBoxLayout, QMainWindow

from editorWnd.env import ENV
from editorWnd.node import GraphicNode
from editorWnd.node_port import ParamPort, OutputPort
from editorWnd.scene import Scene
from editorWnd.view import View


class VisualGraphWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('可视化编程编辑器')
        self.resize(1200, 700)
        editor = Editor(self)
        self.setCentralWidget(editor)
        self.__center()
        # 菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件(&F)')
        self.new_action = QAction(text='&新建', parent=self)
        self.open_action = QAction(text='&打开', parent=self)
        self.save_action = QAction(text='&保存', parent=self)
        file_menu.addActions([self.new_action, self.open_action, self.save_action])

        edit_menu = menubar.addMenu('编辑(&E)')
        self.copy_action = QAction(text='&复制', parent=self)
        self.paste_action = QAction(text='&粘贴', parent=self)
        self.cut_action = QAction(text='&剪切', parent=self)
        self.undo_action = QAction(text='&撤销', parent=self)
        self.redo_action = QAction(text='&重做', parent=self)
        edit_menu.addActions([self.copy_action, self.paste_action, self.cut_action, self.undo_action, self.redo_action])

        selection_menu = menubar.addMenu('选择(&S)')

        run_menu = menubar.addMenu('运行(&R)')

        help_menu = menubar.addMenu('帮助(&H)')

        self.show()

    def __center(self):
        screen = QGuiApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))


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
        """
        右键添加节点
        :param mouse_pos: 鼠标点击的位置
        :return:
        """
        self.debug_add_custom_node((mouse_pos.x(), mouse_pos.y()))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            # self.right_click_add_node(self.view.mapToScene(event.pos()))  # 将鼠标位置从屏幕映射到scene中的位置
            pass
        else:
            super().mousePressEvent(event)
