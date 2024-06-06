import inspect
import os
import sys
from collections import defaultdict
from typing import Type, Dict, List

import editorWnd.nodes
from editorWnd.node import Node
from editorWnd.node_lib import NodeClsLib


class ENV:
    @staticmethod
    def init_node_env():
        node_cls_lst: List[Type] = []
        # 获得nodes软件包下的文件名，并导入
        path_folder = os.path.dirname(editorWnd.nodes.__file__)
        for module in os.listdir(path_folder):
            if not module.endswith('.py') or module == '__init__.py':
                continue
            __import__(f'editorWnd.nodes.{module[:-3]}', locals(), globals())  # 导入模块，在locals和globals中添加模块的名字和对象
        # 对已导入的nodes包下的文件名进行遍历
        for module_name, _ in inspect.getmembers(editorWnd.nodes, inspect.ismodule):
            for cls_name, cls in inspect.getmembers(sys.modules[f'editorWnd.nodes.{module_name}'], inspect.isclass):
                if cls_name != 'Node' and issubclass(cls, Node):
                    node_cls_lst.append(cls)
        NodeClsLib.register_nodes(node_cls_lst)

    @staticmethod
    def get_registered_node_cls() -> List[Type]:
        return NodeClsLib.node_cls_list

    @staticmethod
    def get_nodelib_json_data() -> Dict[str, Dict[str, Type]]:
        data = defaultdict(dict)
        for cls in ENV.get_registered_node_cls():
            pkg_name = cls.pkg_name
            node_title = cls.node_title
            data[pkg_name][node_title] = cls
        return data
