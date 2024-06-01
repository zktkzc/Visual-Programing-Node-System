from editorWnd.node import Node, NodeInput, NodeOutput
from editorWnd.node_port import Pin


class AddNode(Node):
    node_title = '加法'
    node_description = '基本运算 加法'
    input_pins = [
        NodeInput(pin_name='输入1', pin_type=Pin.PinType.DATA, pin_class='float', pin_color='#99ff22'),
        NodeInput(pin_name='输入2', pin_type=Pin.PinType.DATA, pin_class='float', pin_color='#99ff22'),
    ]
    output_pins = [
        NodeOutput(pin_name='结果', pin_type=Pin.PinType.DATA, pin_class='float', pin_color='#99ff22'),
    ]


def run_node(self):
    sum = 0
    for pin in self._input_pins:
        sum += pin.get_pin_value()
    self._output_pins[0].set_pin_value(sum)
