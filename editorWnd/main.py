import sys
import os

from PySide6.QtWidgets import QApplication
from editorWnd.editor import VisualGraphWindow

if __name__ == '__main__':
    # 把运行目录切换到项目根目录
    os.chdir(os.path.dirname(os.path.dirname(__file__)))
    app = QApplication([])
    window = VisualGraphWindow()
    sys.exit(app.exec())
