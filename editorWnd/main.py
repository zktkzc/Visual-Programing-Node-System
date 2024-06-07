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
    
    QMenu::item::disabled {
        color: #888888;
    }
    
    QMenu::item::disabled::selected {
        background-color: transparent;
    }
    
    QMenu::item:selected {
        background-color: #888888;
    }
    
    QWidget {
        background-color: #151515;
        margin: 0px;
        padding: 0px;
    }
    
    QTabBar::tab {
        background-color: #151515;
        color: #888888;
        border-top: 1px solid white;
        border-left: 1px solid white;
        border-right: 1px solid white;
        font-size: 14px;
        width: 100px;
        height: 20px;
        spacing: 10px;
    }
    
    QTabBar::tab:selected {
        background-color: #a8a8a8;
        color: black;
        border-left: none;
        border-right: none;
    }
    
    QTabWidget::tab-bar {
        background-color: #151515;
        left: 10px;
    }
    
    QTabWidget::pane {
        border: 1px solid gray;
    }
'''

if __name__ == '__main__':
    # 把运行目录切换到项目根目录
    os.chdir(os.path.dirname(os.path.dirname(__file__)))
    app = QApplication([])
    window = VisualGraphWindow()
    window.setStyleSheet(GLOBAL_STYLESHEET)
    sys.exit(app.exec())
