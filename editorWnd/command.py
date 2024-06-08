from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Any, Union

from PySide6.QtGui import QUndoCommand
from PySide6.QtWidgets import QGraphicsItem

from editorWnd.edge import NodeEdge
from editorWnd.node import Node, GraphicNode

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


class PasteCommand(QUndoCommand):
    def __init__(self, editor: Editor, data: Dict[str, List[Dict[str, Any]]], is_cut: bool):
        super().__init__()
        self.editor: Editor = editor
        self.data = data
        self.is_cut = is_cut
        self.items: List[Union[Node, GraphicNode, NodeEdge]] = []
        self.selected_items: List[QGraphicsItem] = []

    def redo(self):
        self.selected_items = self.editor.view.unselected_selected_items()
        self.items = self.editor.view.itemfy_json_string(
            data=self.data,
            mouse_position=self.editor.map_mouse_to_scene(),
            is_cut=self.is_cut
        )

    def undo(self):
        self.editor.select_items(self.selected_items)
        for item in self.items.copy():
            item.remove_self()
