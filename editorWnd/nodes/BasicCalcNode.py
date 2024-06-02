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
        for pin in self.input_pins:
            sum += pin.get_pin_value()
        self.output_pins[0].set_pin_value(sum)


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
        diff = self.input_pins[0]
        for pin in self.input_pins[1:]:
            diff -= pin.get_pin_value()
        self.output_pins[0].set_pin_value(diff)


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
        result = self.input_pins[0]
        for pin in self.input_pins[1:]:
            result *= pin.get_pin_value()
        self.output_pins[0].set_pin_value(result)


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
        result = self.input_pins[0]
        for pin in self.input_pins[1:]:
            if pin.get_pin_value() == 0:
                print('Node: the second input is zero, cannot divide by zero')
                return
            result /= pin.get_pin_value()
        self.output_pins[0].set_pin_value(result)


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
        if self.input_pins[0].get_pin_value() > self.input_pins[1].get_pin_value():
            self.output_pins[0].set_pin_value(True)
        else:
            self.output_pins[0].set_pin_value(False)
        self.output_pins[1].set_pin_value(self.input_pins[0].get_pin_value())
        self.output_pins[2].set_pin_value(self.input_pins[1].get_pin_value())


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
    ]

    def run_node(self):
        if self.input_pins[0].get_pin_value() < self.input_pins[1].get_pin_value():
            self.output_pins[0].set_pin_value(True)
        else:
            self.output_pins[0].set_pin_value(False)
