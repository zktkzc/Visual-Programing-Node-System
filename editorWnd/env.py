from collections import defaultdict
from typing import Type

from node_lib import NodeClsLib
from nodes.BasicCalcNode import AddNode
from nodes.BranchNode import BranchNode


class ENV:
    @staticmethod
    def init_node_env():
        NodeClsLib.register_nodes([BranchNode, AddNode])

    @staticmethod
    def get_registered_node_cls() -> list[Type]:
        return NodeClsLib.node_cls_list

    @staticmethod
    def get_nodelib_json_data() -> dict[str, dict[str, Type]]:
        data = defaultdict(dict)
        for cls in ENV.get_registered_node_cls():
            pkg_name = cls.pkg_name
            node_title = cls.node_title
            data[pkg_name][node_title] = cls
        return data
