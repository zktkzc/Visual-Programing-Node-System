import sys

from PySide6.QtWidgets import QApplication
from editor import Editor

if __name__ == '__main__':
    app = QApplication([])
    editor = Editor()
    sys.exit(app.exec())