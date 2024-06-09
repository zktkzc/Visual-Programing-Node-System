from __future__ import annotations
from typing import TYPE_CHECKING
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics, QFont, QMouseEvent
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout

if TYPE_CHECKING:
    from editorWnd.group import NodeGroup

class EditableLabel(QWidget):
    def __init__(self, text: str = '', group: NodeGroup = None):
        super().__init__(None)
        self._text = text
        self._group = group
        self._label = QLabel(self)
        self._label.setText(self._text)
        self._label.setFont(QFont('微软雅黑', 14))
        self._line_edit = QLineEdit(self)
        self._line_edit.setHidden(True)
        self._line_edit.setFont(QFont('微软雅黑', 14))
        self._line_edit.returnPressed.connect(self.update_label)
        self._line_edit.textEdited.connect(self.__enable_edit_mode)
        self._line_edit.textChanged.connect(self.__update_line_edit_width)
        self._v_layout = QVBoxLayout(self)
        self.setLayout(self._v_layout)
        self._v_layout.setContentsMargins(0, 0, 0, 0)
        self._v_layout.addWidget(self._label)
        self._v_layout.addWidget(self._line_edit)
        self._is_edit_mode: bool = False
        self._fm = QFontMetrics(QFont('微软雅黑', 14))
        self._label.setStyleSheet('''
            color: #ddd;
        ''')
        self._line_edit.setStyleSheet('''
            color: #fff;
        ''')
        self.setStyleSheet('''
            border: none;
            background-color: transparent;
        ''')

    def label_double_clicked(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.__enable_edit_mode()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.__cancel_edit()
        super().keyPressEvent(event)

    def __update_line_edit_width(self, text):
        self._line_edit.setFixedWidth(self._fm.boundingRect(text).width() + 20)

    def update_label(self):
        self._is_edit_mode = False
        self._label.setText(self._line_edit.text())
        self._line_edit.setHidden(True)
        self._label.setHidden(False)
        self._group.set_title(self._label.text())

    def __cancel_edit(self):
        self._is_edit_mode = False
        self._line_edit.setHidden(True)
        self._label.setHidden(False)

    def __enable_edit_mode(self):
        """
        鼠标双击，进入编辑模式
        :return:
        """
        if self._is_edit_mode:
            return
        self._is_edit_mode = True
        self._label.setHidden(True)
        self._line_edit.setText(self._label.text())
        self._line_edit.setHidden(False)
        self._line_edit.setFocus()
        self._line_edit.selectAll()

    def get_text(self) -> str:
        return self._label.text()
