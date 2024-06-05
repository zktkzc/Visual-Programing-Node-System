from editorWnd.node import Node
from editorWnd.node_port import NodeOutput, NodeInput, Pin
from editorWnd.dtypes import DTypes


class Integer2FloatNode(Node):
    pkg_name = '节点转换'
    node_title = '整数转浮点数'
    node_description = '将整数转换为浮点数'
    input_pins = [
        NodeInput(pin_type=Pin.PinType.DATA, pin_name='整数', pin_class=DTypes.Integer)
    ]
    output_pins = [
        NodeOutput(pin_type=Pin.PinType.DATA, pin_name='浮点数', pin_class=DTypes.Float)
    ]

    def run_node(self):
        self.output(0, float(self.input(0)))


class Float2IntegerNode(Node):
    pkg_name = '节点转换'
    node_title = '浮点数转整数'
    node_description = '将浮点数转换为整数'
    input_pins = [
        NodeInput(pin_type=Pin.PinType.DATA, pin_name='浮点数', pin_class=DTypes.Float)
    ]
    output_pins = [
        NodeOutput(pin_type=Pin.PinType.DATA, pin_name='整数', pin_class=DTypes.Integer)
    ]

    def run_node(self):
        self.output(0, int(self.input(0)))


class Bool2StringNode(Node):
    pkg_name = '节点转换'
    node_title = '布尔值转字符串'
    node_description = '将布尔值转换为字符串'
    input_pins = [
        NodeInput(pin_type=Pin.PinType.DATA, pin_name='布尔值', pin_class=DTypes.Boolean)
    ]
    output_pins = [
        NodeOutput(pin_type=Pin.PinType.DATA, pin_name='字符串', pin_class=DTypes.String)
    ]

    def run_node(self):
        self.output(0, str(self.input(0)))


class Integer2StringNode(Node):
    pkg_name = '节点转换'
    node_title = '整数转字符串'
    node_description = '将整数转换为字符串'
    input_pins = [
        NodeInput(pin_type=Pin.PinType.DATA, pin_name='整数', pin_class=DTypes.Integer)
    ]
    output_pins = [
        NodeOutput(pin_type=Pin.PinType.DATA, pin_name='字符串', pin_class=DTypes.String)
    ]

    def run_node(self):
        self.output(0, str(self.input(0)))


class Float2StringNode(Node):
    pkg_name = '节点转换'
    node_title = '浮点数转字符串'
    node_description = '将浮点数转换为字符串'
    input_pins = [
        NodeInput(pin_type=Pin.PinType.DATA, pin_name='浮点数', pin_class=DTypes.Float)
    ]
    output_pins = [
        NodeOutput(pin_type=Pin.PinType.DATA, pin_name='字符串', pin_class=DTypes.String)
    ]

    def run_node(self):
        self.output(0, str(self.input(0)))


class Class2StringNode(Node):
    pkg_name = '节点转换'
    node_title = '类转字符串'
    node_description = '将类转换为字符串'
    input_pins = [
        NodeInput(pin_type=Pin.PinType.DATA, pin_name='对象', pin_class=DTypes.Class)
    ]
    output_pins = [
        NodeOutput(pin_type=Pin.PinType.DATA, pin_name='字符串', pin_class=DTypes.String)
    ]

    def run_node(self):
        self.output(0, str(self.input(0)))