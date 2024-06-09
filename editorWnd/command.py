from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Any, Union

from PySide6.QtGui import QUndoCommand
from PySide6.QtWidgets import QGraphicsItem

from editorWnd.edge import NodeEdge
from editorWnd.node import Node, GraphicNode
from editorWnd.group import NodeGroup

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


class DelCommand(QUndoCommand):
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
            elif isinstance(item, NodeGroup):
                self.editor.readd_group(item)

    def redo(self):
        if len(self.items) > 0:
            for item in self.items:
                if isinstance(item, Node):
                    for edge in item.edges:
                        if edge not in self.items:
                            self.items.append(edge)
                    item.remove_self()
                elif isinstance(item, NodeEdge):
                    item.remove_self()
                elif isinstance(item, NodeGroup):
                    item.remove_self()


class GroupCommand(QUndoCommand):
    def __init__(self, editor: Editor):
        super().__init__()
        self._editor = editor
        self._group: Union[NodeGroup, None] = None

    def redo(self):
        # 获取选中的元素
        selected_items = self._editor.view.get_selected_items()
        nodes: List[Union[GraphicNode, Node]] = []
        edges: List[NodeEdge] = []
        top, bottom, left, right = None, None, None, None
        # 获取最上、最下、最左、最右的坐标
        if len(selected_items) > 0:
            for item in selected_items:
                if isinstance(item, GraphicNode):
                    nodes.append(item)
                elif isinstance(item, NodeEdge):
                    edges.append(item)
        if len(nodes) == 0:
            return
        for edge in edges.copy():
            if edge.src_port.parent_node not in nodes or edge.dest_port.parent_node not in nodes:
                edges.remove(edge)
        items = []
        items.extend(nodes)
        items.extend(edges)
        self._group = self._editor.view.add_node_group(items=items, title='节点组')

    def undo(self):
        self._editor.view.delete_node_group(self._group)
