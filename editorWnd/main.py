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
        color: #c4c4c4;
    }
    
    QMenuBar::item {
        padding: 1px 4px;
        background-color: transparent;
    }
    
    QMenuBar::item:selected {
        background-color: #a8a8a8;
        color: white;
    }
    
    QMenuBar::item:pressed {
        background-color: #888888;
    }
    
    QMenu {
        background-color: #151515;
        color: #c4c4c4;
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
        color: white;
    }
    
    QWidget {
        background-color: #151515;
        margin: 0px;
        padding: 0px;
        border: none;
    }
    
    QTabBar::tab {
        background-color: #313131;
        color: #c4c4c4;
        border: none;
        font-size: 14px;
        min-width: 15ex;
        height: 20px;
        spacing: 10px;
        padding: 5px;
    }
    
    QTabBar::tab:selected {
        background-color: #151515;
        padding: 5px;
    }
    
    QTabWidget::tab-bar {
        border-bottom: 1px solid #101010;
    }
    
    QTabWidget::pane {
        border-top: 7px solid qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #151515, stop: 0.4 #101010,
        stop: 0.5 #010101, stop: 1 #313131);
    }
'''

if __name__ == '__main__':
    # 把运行目录切换到项目根目录
    os.chdir(os.path.dirname(os.path.dirname(__file__)))
    app = QApplication([])
    window = VisualGraphWindow()
    window.setStyleSheet(GLOBAL_STYLESHEET)
    sys.exit(app.exec())
