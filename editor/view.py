'''
QGraphicsView的子类，是scene的容器
'''

from PySide6.QtWidgets import QGraphicsView


class View(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(parent)
        self._scene = scene
        self.setScene(self._scene)
