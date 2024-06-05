from editorWnd.dtypes import DTypes
from editorWnd.node import Node
from editorWnd.node_port import NodeInput, NodeOutput, Pin


class IntegerNode(Node):
    pkg_name = '输入节点'
    node_title = '整数'
    node_description = '输入一个整数'
    input_pins = [
        NodeInput(pin_class=DTypes.Integer, pin_type=Pin.PinType.DATA, hide_icon=True)
    ]
    output_pins = [
        NodeOutput(pin_class=DTypes.Integer, pin_type=Pin.PinType.DATA)
    ]

    def run_node(self):
        self.output(0, self.input(0))


class FloatNode(Node):
    pkg_name = '输入节点'
    node_title = '浮点数'
    node_description = '输入一个浮点数'
    input_pins = [
        NodeInput(pin_class=DTypes.Float, pin_type=Pin.PinType.DATA, hide_icon=True)
    ]
    output_pins = [
        NodeOutput(pin_class=DTypes.Float, pin_type=Pin.PinType.DATA)
    ]

    def run_node(self):
        self.output(0, self.input(0))


class StringNode(Node):
    pkg_name = '输入节点'
    node_title = '字符串'
    node_description = '输入一个字符串'
    input_pins = [
        NodeInput(pin_class=DTypes.String, pin_type=Pin.PinType.DATA, hide_icon=True)
    ]
    output_pins = [
        NodeOutput(pin_class=DTypes.String, pin_type=Pin.PinType.DATA)
    ]

    def run_node(self):
        self.output(0, self.input(0))


class BooleanNode(Node):
    pkg_name = '输入节点'
    node_title = '布尔'
    node_description = '输入一个布尔值'
    input_pins = [
        NodeInput(pin_class=DTypes.Boolean, pin_type=Pin.PinType.DATA, hide_icon=True)
    ]
    output_pins = [
        NodeOutput(pin_class=DTypes.Boolean, pin_type=Pin.PinType.DATA)
    ]

    def run_node(self):
        self.output(0, self.input(0))


class StringArrayNode(Node):
    pkg_name = '输入节点'
    node_title = '字符串数组'
    node_description = '输入一个字符串数组'
    input_pins = [
        NodeInput(pin_class=DTypes.String, pin_type=Pin.PinType.DATA, hide_icon=True),
        NodeInput(pin_class=DTypes.String, pin_type=Pin.PinType.DATA, hide_icon=True),
        NodeInput(pin_class=DTypes.String, pin_type=Pin.PinType.DATA, hide_icon=True),
        NodeInput(pin_class=DTypes.String, pin_type=Pin.PinType.DATA, hide_icon=True),
    ]
    output_pins = [
        NodeOutput(pin_class=DTypes.Array, pin_type=Pin.PinType.DATA),
    ]

    def run_node(self):
        self.output(0, [self.input(i) for i in range(len(self.in_ports))])
