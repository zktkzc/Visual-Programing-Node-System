from __future__ import annotations

import sys

from node import Node, NodeInput, NodeOutput
from node_port import Pin

sys.path.append('..')


class BranchNode(Node):
    node_title = 'Branch'
    node_description = 'Execute based on input condition'
    input_pins = [
        NodeInput(pin_type=Pin.PinType.EXEC),
        NodeInput(pin_name='Condition', pin_class='bool', pin_color='#ff3300', pin_type=Pin.PinType.DATA)
    ]
    output_pins = [
        NodeOutput(pin_type=Pin.PinType.EXEC, pin_name='True'),
        NodeOutput(pin_name='False', pin_type=Pin.PinType.EXEC)
    ]

    def run_node(self):
        super().run_node()
