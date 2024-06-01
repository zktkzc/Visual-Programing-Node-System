from editorWnd.node import Node, NodeInput, NodeOutput
from editorWnd.node_port import Pin


class BranchNode(Node):
    pkg_name = '控制结构'
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
        if self.input_pins[1]:
            self.exec_output(0)
        else:
            self.exec_output(1)

class ForEachNode(Node):
    pkg_name = '控制结构'
    node_title = '遍历'
    node_description = '遍历可迭代对象中的每一个元素'
    input_pins = [
        NodeInput(pin_type=Pin.PinType.EXEC),
        NodeInput(pin_name='开始', pin_class='int', pin_color='#00ffee', pin_type=Pin.PinType.DATA),
        NodeInput(pin_name='结束', pin_class='int', pin_color='#00ffee', pin_type=Pin.PinType.DATA),
        NodeInput(pin_name='数组', pin_class='list', pin_color='#345678', pin_type=Pin.PinType.DATA),
    ]
    output_pins = [
        NodeOutput(pin_type=Pin.PinType.EXEC, pin_name='循环体'),
        NodeOutput(pin_type=Pin.PinType.DATA, pin_name='索引', pin_class='int', pin_color='#00ffee'),
        NodeOutput(pin_type=Pin.PinType.DATA, pin_name='元素', pin_class='int', pin_color='#345678'),
        NodeOutput(pin_type=Pin.PinType.EXEC, pin_name='完成'),
    ]

    def run_node(self):
        pass