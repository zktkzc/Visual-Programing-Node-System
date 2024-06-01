from editorWnd.node import Node, NodeInput, NodeOutput
from editorWnd.node_port import Pin


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
        if self._input_pins[1]:
            self.exec_output(0)
        else:
            self.exec_output(1)
