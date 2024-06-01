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
