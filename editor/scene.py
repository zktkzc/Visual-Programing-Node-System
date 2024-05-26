'''
QGraphicsScene的子类
'''

from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtGui import QBrush, QColor
from config import EditorConfig

class Scene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setBackgroundBrush(QBrush(QColor('#212121')))
        self._width = EditorConfig.EDITOR_SCENE_WIDTH
        self._height = EditorConfig.EDITOR_SCENE_HEIGHT
        # 设置背景大小
        self.setSceneRect(self._width/2, self._height/2, self._width, self._height)