"""
编辑器主体
"""
from __future__ import annotations

import os
from functools import partial
from typing import List, Union, Dict

from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QGuiApplication, QAction, QKeySequence
from PySide6.QtWidgets import QWidget, QBoxLayout, QMainWindow, QFileDialog, QTabWidget, QLayout

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
        self.editor = Editor(self)
        self.setCentralWidget(self.editor)
        self.__center()
        # 菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件(&F)')
        self.new_graph_action = QAction(text='&新建画布', parent=self)
        self.new_graph_action.setShortcuts([QKeySequence('Ctrl+N')])
        self.new_graph_action.triggered.connect(self.add_a_tab)
        file_menu.addAction(self.new_graph_action)
        self.new_window_action = QAction(text='&新建窗口', parent=self)
        self.new_window_action.setShortcuts([QKeySequence('Ctrl+Shift+N')])
        file_menu.addAction(self.new_window_action)
        file_menu.addSeparator()
        self.open_action = QAction(text='&打开', parent=self)
        self.open_action.setShortcuts([QKeySequence('Ctrl+O')])
        self.open_action.triggered.connect(self.__open_with_dialog)
        file_menu.addAction(self.open_action)
        self.recent_menu = file_menu.addMenu('&最近打开')
        self.recent_menu.aboutToShow.connect(self.__show_recent_files)
        self.clear_recent_files_action = QAction(text='清除历史记录', parent=self)
        self.clear_recent_files_action.triggered.connect(self.__clear_recent_files)
        file_menu.addSeparator()
        self.set_workspace_action = QAction(text='&设置工作区', parent=self)
        file_menu.addAction(self.set_workspace_action)
        file_menu.addSeparator()
        self.save_action = QAction(text='&保存', parent=self)
        self.save_action.setShortcuts([QKeySequence('Ctrl+S')])
        self.save_action.triggered.connect(self.__save)
        file_menu.addAction(self.save_action)
        self.save_as_action = QAction(text='&另存为', parent=self)
        self.save_as_action.setShortcuts([QKeySequence('Ctrl+Shift+S')])
        self.save_as_action.triggered.connect(self.__save_as)
        file_menu.addAction(self.save_as_action)
        self.save_all_action = QAction(text='&全部保存', parent=self)
        self.save_all_action.setShortcuts([QKeySequence('Ctrl+Alt+S')])
        self.save_all_action.triggered.connect(self.__save_all)
        file_menu.addAction(self.save_all_action)
        file_menu.addSeparator()
        self.quit_action = QAction(text='&退出', parent=self)
        self.quit_action.setShortcuts([QKeySequence('Alt+F4')])
        file_menu.addAction(self.quit_action)

        edit_menu = menubar.addMenu('编辑(&E)')
        self.copy_action = QAction(text='&复制', parent=self)
        self.paste_action = QAction(text='&粘贴', parent=self)
        self.cut_action = QAction(text='&剪切', parent=self)
        edit_menu.addSeparator()
        self.undo_action = QAction(text='&撤销', parent=self)
        self.redo_action = QAction(text='&重做', parent=self)
        edit_menu.addActions([self.copy_action, self.paste_action, self.cut_action, self.undo_action, self.redo_action])

        selection_menu = menubar.addMenu('选择(&S)')

        run_menu = menubar.addMenu('运行(&R)')

        help_menu = menubar.addMenu('帮助(&H)')

        # 上次打开的路径
        self._last_open_path: str = os.getcwd()
        # 最近文件列表，只记录文件的绝对路径
        self.recent_files: List[str] = []

        # tab栏
        self.tabs = []
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)
        self.tab_widget.setTabsClosable(True)
        self.add_a_tab()  # 默认添加一个tab
        self.tab_widget.currentChanged.connect(self.tab_changed)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_index: int = 0
        self.opened_files: Dict[str, int] = {}

        self.show()

    def close_tab(self, index: int):
        self.tab_widget.removeTab(index)
        self.tabs.pop(index)
        if self.tab_widget.count() == 0:
            self.add_a_tab()

    def record_file_opened(self, filepath: str, index: int):
        self.opened_files[filepath] = index

    def tab_changed(self, index: int):
        if len(self.tabs) > 0:
            self.tab_index = index
            self.editor = self.tabs[index]

    def add_a_tab(self, filepath: str = ''):
        tab_view = Editor(self)
        if filepath == ''or isinstance(filepath, int):
            tab_title = f'未命名-{len(self.tabs) + 1}'
        else:
            tab_title = os.path.basename(filepath)
        self.tab_widget.addTab(tab_view, tab_title)
        self.tabs.append(tab_view)
        self.set_current_editor(tab_view, self.tab_widget.count() - 1)

    def set_current_editor(self, editor: Editor = None, index: int = 0):
        self.editor = editor
        self.tab_widget.setCurrentWidget(self.tabs[index])

    def __clear_recent_files(self):
        self.recent_files = []
        self.__show_recent_files()

    def __load_recent_file(self, filepath: str):
        self.__open(filepath)

    def __show_recent_files(self):
        self.recent_menu.clear()  # 清除菜单项
        actions: List[QAction] = []
        for filepath in self.recent_files:
            action = QAction(text=filepath, parent=self)
            action.triggered.connect(partial(self.__load_recent_file, filepath))
            actions.append(action)
        if len(actions) > 0:
            self.recent_menu.addActions(actions)
        else:
            no_recent_file = QAction(text='没有最近打开的文件', parent=self)
            no_recent_file.setDisabled(True)
            self.recent_menu.addAction(no_recent_file)
        self.recent_menu.addSeparator()
        self.recent_menu.addAction(self.clear_recent_files_action)

    def __add_to_recent_files(self, filepath: str):
        if filepath in set(self.recent_files):
            self.recent_files.remove(filepath)
        self.recent_files.insert(0, filepath)

    def __save_all(self):
        for tab in self.tabs:
            self.__save_in_tab(tab)

    def __save_in_tab(self, tab: Editor):
        if not tab.save_graph():
            filepath, filetype = QFileDialog.getSaveFileName(self, '保存',
                                                             os.path.join(os.getcwd(), 'untitled.vgf'),
                                                             'Visual Graph File(*.vgf)')
            if filepath == '':
                # 取消
                return
            self.tab_widget.setTabText(self.tab_index, os.path.basename(filepath))
            self.record_file_opened(filepath, self.tab_index)
            tab.save_graph_as(filepath)
            self.__add_to_recent_files(filepath)

    def __save(self):
        if not self.editor.save_graph():
            filepath, filetype = QFileDialog.getSaveFileName(self, '保存', os.path.join(os.getcwd(), 'untitled.vgf'),
                                                             'Visual Graph File(*.vgf)')
            if filepath == '':
                # 取消
                return
            self.tab_widget.setTabText(self.tab_index, os.path.basename(filepath))
            self.record_file_opened(filepath, self.tab_index)
            self.editor.save_graph_as(filepath)
            self.__add_to_recent_files(filepath)

    def __save_as(self):
        filepath, filetype = QFileDialog.getSaveFileName(self, '另存为', os.path.join(os.getcwd(), 'untitled.vgf'),
                                                         'Visual Graph File(*.vgf)')
        if filepath == '':
            # 取消
            return
        self.editor.save_graph_as(filepath)
        self.__add_to_recent_files(filepath)

    def __open_with_dialog(self):
        filepath, filetype = QFileDialog.getOpenFileName(self, '打开', self._last_open_path, 'Visual Graph File(*.vgf)')
        if filepath == '':
            return
        self.__open(filepath)

    def __open(self, filepath: str):
        index = self.opened_files.get(filepath, -1)
        if index != -1:
            self.tab_widget.setCurrentIndex(index)
            return
        if self.editor.view.get_saved_path() != '':
            # 创建一个新的tab
            self.add_a_tab(filepath=filepath)
        else:
            self.tab_widget.setTabText(self.tab_index, os.path.basename(filepath))
        self.editor.open_graph(filepath)
        self._last_open_path = os.path.dirname(filepath)
        self.__add_to_recent_files(filepath)
        self.record_file_opened(filepath, self.tab_index)

    def __center(self):
        screen = QGuiApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))


class Editor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene: Union[Scene, None] = None
        self.view: Union[View, None] = None
        self.layout: Union[QLayout, None] = None
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
        param_ports: list[ParamPort] = [
            ParamPort('宽度', 'float', '#99ff22'),
            ParamPort('高度', 'float', '#99ff22'),
            ParamPort('计数', 'int', '#00ffee')
        ]

        output_params: list[OutputPort] = [
            OutputPort('面积', 'float', '#99ff22'),
            OutputPort('数量', 'int', '#00ffee')
        ]

        node = GraphicNode(title='面积', param_ports=param_ports, output_ports=output_params, is_pure=False)
        self.view.add_node(node, pos)

    def center(self):
        if len(self.view.get_nodes()) > 0:
            pos = self.view.get_nodes()[0].scenePos()
            width, height = self.view.geometry().width(), self.view.geometry().height()
            self.view.centerOn(QPointF(pos.x() + width / 2 - 100, pos.y() + height / 2 - 100))

    def open_graph(self, filepath: str):
        self.view.load_graph(filepath)
        self.center()

    def save_graph(self) -> bool:
        return self.view.save_directly()

    def save_graph_as(self, filepath: str):
        self.view.save_graph(filepath)

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
