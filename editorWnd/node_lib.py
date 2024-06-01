from typing import Type


class NodeClsLib:
    node_cls_list: list[Type] = []

    @staticmethod
    def register_nodes(node_cls: Type | list[Type]):
        if isinstance(node_cls, list):
            NodeClsLib.node_cls_list.extend(node_cls)
        else:
            NodeClsLib.node_cls_list.append(node_cls)
