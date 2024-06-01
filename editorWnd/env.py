import inspect
import sys
from collections import defaultdict
from typing import Type

import nodes
from editorWnd.node import Node
from node_lib import NodeClsLib


class ENV:
    @staticmethod
    def init_node_env():
        node_cls_lst: list[Type] = []
        for module_name, _ in inspect.getmembers(nodes, inspect.ismodule):
            for cls_name, cls in inspect.getmembers(sys.modules[f'nodes.{module_name}'], inspect.isclass):
                if cls_name != 'Node' and issubclass(cls, Node):
                    node_cls_lst.append(cls)
        NodeClsLib.register_nodes(node_cls_lst)

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
