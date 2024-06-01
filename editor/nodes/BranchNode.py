from __future__ import annotations

import sys

from node import Node, NodeInput, NodeOutput
from node_port import Pin

sys.path.append('..')


class BranchNode(Node):
    node_title = '分支'
    node_description = '基于输入条件进行执行'
    input_pins = [
        NodeInput(pin_type=Pin.PinType.EXEC),
        NodeInput(pin_name='条件', pin_class='bool', pin_color='#ff3300', pin_type=Pin.PinType.DATA)
    ]
    output_pins = [
        NodeOutput(pin_type=Pin.PinType.EXEC, pin_name='真'),
        NodeOutput(pin_name='假', pin_type=Pin.PinType.EXEC),
    ]

    def run_node(self):
        super().run_node()
