from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtGui import QUndoCommand

from editorWnd.edge import NodeEdge
from editorWnd.node import Node

if TYPE_CHECKING:
    from editorWnd.editor import Editor


class CutCommand(QUndoCommand):
    def __init__(self, editor: Editor):
        super().__init__()
        self.editor: Editor = editor
        self.items = self.editor.view.get_selected_items()

    def undo(self):
        for item in self.items:
            if isinstance(item, Node):
                self.editor.readd_node(item)
            elif isinstance(item, NodeEdge):
                self.editor.readd_edge(edge=item)

    def redo(self):
        for item in self.items:
            if isinstance(item, Node):
                for edge in item.edges:
                    if edge not in self.items:
                        self.items.append(edge)
                item.remove_self()
