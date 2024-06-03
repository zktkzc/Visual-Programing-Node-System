from editorWnd.dtypes import DTypes
from editorWnd.node import Node
from editorWnd.node_port import Pin, NodeInput, NodeOutput


class AddNode(Node):
    pkg_name = '基本运算'
    node_title = '加法'
    node_description = '基本运算 加法'
    input_pins = [
        NodeInput(pin_name='输入1', pin_type=Pin.PinType.DATA, pin_class=DTypes.Float),
        NodeInput(pin_name='输入2', pin_type=Pin.PinType.DATA, pin_class=DTypes.Float),
    ]
    output_pins = [
        NodeOutput(pin_name='结果', pin_type=Pin.PinType.DATA, pin_class=DTypes.Float),
    ]

    def run_node(self):
        sum = 0
        for index in range(len(self.in_ports)):
            sum += self.input(index)
        self.output(0, sum)


class MinusNode(Node):
    pkg_name = '基本运算'
    node_title = '减法'
    node_description = '基本运算 减法'
    input_pins = [
        NodeInput(pin_name='输入1', pin_type=Pin.PinType.DATA, pin_class=DTypes.Float),
        NodeInput(pin_name='输入2', pin_type=Pin.PinType.DATA, pin_class=DTypes.Float), ]
    output_pins = [
        NodeOutput(pin_name='结果', pin_type=Pin.PinType.DATA, pin_class=DTypes.Float),
    ]

    def run_node(self):
        diff = self.input(0)
        for index in range(1, len(self.in_ports)):
            diff -= self.input(index)
        self.output(0, diff)


class MultiplyNode(Node):
    pkg_name = '基本运算'
    node_title = '乘法'
    node_description = '基本运算 乘法'
    input_pins = [
        NodeInput(pin_name='输入1', pin_type=Pin.PinType.DATA, pin_class=DTypes.Float),
        NodeInput(pin_name='输入2', pin_type=Pin.PinType.DATA, pin_class=DTypes.Float),
    ]
    output_pins = [
        NodeOutput(pin_name='结果', pin_type=Pin.PinType.DATA, pin_class=DTypes.Float),
    ]

    def run_node(self):
        result = self.input(0)
        for index in range(1, len(self.in_ports)):
            result *= self.input(index)
        self.output(0, result)


class DivideNode(Node):
    pkg_name = '基本运算'
    node_title = '除法'
    node_description = '基本运算 除法'
    input_pins = [
        NodeInput(pin_name='输入1', pin_type=Pin.PinType.DATA, pin_class=DTypes.Float),
        NodeInput(pin_name='输入2', pin_type=Pin.PinType.DATA, pin_class=DTypes.Float),
    ]
    output_pins = [
        NodeOutput(pin_name='结果', pin_type=Pin.PinType.DATA, pin_class=DTypes.Float),
    ]

    def run_node(self):
        result = self.input(0)
        for index in range(1, len(self.in_ports)):
            if self.input(index) == 0:
                print('除法节点: 除数不能为0')
                return
            result /= self.input(index)
        self.output(0, result)


class GreaterNode(Node):
    pkg_name = '比较运算'
    node_title = '大于'
    node_description = '比较运算 大于'
    input_pins = [
        NodeInput(pin_name='输入1', pin_type=Pin.PinType.DATA, pin_class=DTypes.Float),
        NodeInput(pin_name='输入2', pin_type=Pin.PinType.DATA, pin_class=DTypes.Float),
    ]
    output_pins = [
        NodeOutput(pin_name='结果', pin_type=Pin.PinType.DATA, pin_class='bool'),
        NodeOutput(pin_name='输出1', pin_type=Pin.PinType.DATA, pin_class=DTypes.Float),
        NodeOutput(pin_name='输出2', pin_type=Pin.PinType.DATA, pin_class=DTypes.Float),
    ]

    def run_node(self):
        if self.input(0) > self.input(1):
            self.output(0, True)
        else:
            self.output(0, False)
        self.output(1, self.input(0))
        self.output(2, self.input(1))


class LessNode(Node):
    pkg_name = '比较运算'
    node_title = '小于'
    node_description = '比较运算 小于'
    input_pins = [
        NodeInput(pin_name='输入1', pin_type=Pin.PinType.DATA, pin_class=DTypes.Float),
        NodeInput(pin_name='输入2', pin_type=Pin.PinType.DATA, pin_class=DTypes.Float),
    ]
    output_pins = [
        NodeOutput(pin_name='结果', pin_type=Pin.PinType.DATA, pin_class='bool'),
        NodeOutput(pin_name='输出1', pin_type=Pin.PinType.DATA, pin_class=DTypes.Float),
        NodeOutput(pin_name='输出2', pin_type=Pin.PinType.DATA, pin_class=DTypes.Float),
    ]

    def run_node(self):
        if self.input(0) < self.input(1):
            self.output(0, True)
        else:
            self.output(0, False)
        self.output(1, self.input(0))
        self.output(2, self.input(1))
