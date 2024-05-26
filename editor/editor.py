'''
编辑器主体
'''

from PySide6.QtWidgets import QWidget, QBoxLayout
from view import View
from scene import Scene


class Editor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_editor()

    def setup_editor(self):
        # 窗口位置以及大小
        self.setGeometry(400, 400, 1000, 720)
        self.setWindowTitle('可视化编程编辑器')
        self.layout = QBoxLayout(QBoxLayout.Direction.LeftToRight, self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # 初始化scene
        self.scene = Scene()
        self.view = View(self.scene, self)
        self.layout.addWidget(self.view)
        self.show()
