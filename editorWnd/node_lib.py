from typing import Type, List, Union


class NodeClsLib:
    node_cls_list: List[Type] = []

    @staticmethod
    def register_nodes(node_cls: Union[Type, List[Type]]):
        if isinstance(node_cls, list):
            NodeClsLib.node_cls_list.extend(node_cls)
        else:
            NodeClsLib.node_cls_list.append(node_cls)
        # 去重
        NodeClsLib.node_cls_list = list(set(NodeClsLib.node_cls_list))
