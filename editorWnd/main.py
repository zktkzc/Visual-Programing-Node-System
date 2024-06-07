import os
import sys

from PySide6.QtWidgets import QApplication

from editorWnd.editor import VisualGraphWindow

GLOBAL_STYLESHEET = '''
    QMainWindow {
        border: 1px solid blue;
    }
    
    QMenuBar {
        background-color: #1e1f1c;
        spacing: 10px;
        font-size: 16px;
        color: white;
    }
    
    QMenuBar::item {
        padding: 1px 4px;
        background-color: transparent;
    }
    
    QMenuBar::item:selected {
        background-color: #a8a8a8；
    }
    
    QMenuBar::item:pressed {
        background-color: #888888;
    }
    
    QMenu {
        background-color: #151515;
        color: white;
        font-size: 16px;
    }
    
    QMenu::separator {
        height: 1px;
        background-color: #999999;
        margin-left: 5px;
        margin-right: 5px;
        margin-top: 5px;
        margin-bottom: 5px;
    }
    
    QMenu::item {
        background-color: transparent;
    }
    
    QMenu::item:selected {
        background-color: #888888;
    }
'''

if __name__ == '__main__':
    # 把运行目录切换到项目根目录
    os.chdir(os.path.dirname(os.path.dirname(__file__)))
    app = QApplication([])
    window = VisualGraphWindow()
    window.setStyleSheet(GLOBAL_STYLESHEET)
    sys.exit(app.exec())
