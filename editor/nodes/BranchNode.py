from __future__ import annotations

import sys

from node import Node, NodeInput, NodeOutput
from node_port import Pin

sys.path.append('..')


class BranchNode(Node):
    def setup_node(self):
        self._node_title = '分支'
        self._node_description = '基于输入条件进行执行'
        self._input_pins = [
            NodeInput(pin_type=Pin.PinType.EXEC),
            NodeInput(pin_name='条件', pin_class='bool', pin_color='#ff3300', pin_type=Pin.PinType.DATA)
        ]
        self._output_pins = [
            NodeOutput(pin_type=Pin.PinType.EXEC, pin_name='真'),
            NodeOutput(pin_name='假', pin_type=Pin.PinType.EXEC),
            NodeOutput(pin_name='假', pin_type=Pin.PinType.DATA),
        ]

    def run_node(self):
        super().run_node()
