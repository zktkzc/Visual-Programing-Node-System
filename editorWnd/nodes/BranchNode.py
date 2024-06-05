from editorWnd.dtypes import DTypes
from editorWnd.node import Node
from editorWnd.node_port import Pin, NodeInput, NodeOutput


class BranchNode(Node):
    pkg_name = '控制结构'
    node_title = '分支'
    node_description = '基于输入条件进行执行'
    input_pins = [
        NodeInput(pin_type=Pin.PinType.EXEC),
        NodeInput(pin_name='条件', pin_class=DTypes.Boolean, pin_type=Pin.PinType.DATA)
    ]
    output_pins = [
        NodeOutput(pin_type=Pin.PinType.EXEC, pin_name='真'),
        NodeOutput(pin_name='假', pin_type=Pin.PinType.EXEC),
    ]

    def run_node(self):
        if self.input(1):
            self.exec_output(0)
        else:
            self.exec_output(1)


class ForEachNode(Node):
    pkg_name = '控制结构'
    node_title = 'ForEach循环'
    node_description = '遍历可迭代对象中的每一个元素'
    input_pins = [
        NodeInput(pin_type=Pin.PinType.EXEC),
        NodeInput(pin_name='开始', pin_class=DTypes.Integer, pin_type=Pin.PinType.DATA),
        NodeInput(pin_name='结束', pin_class=DTypes.Integer, pin_type=Pin.PinType.DATA),
        NodeInput(pin_name='步长', pin_class=DTypes.Integer, pin_type=Pin.PinType.DATA),
        NodeInput(pin_name='数组', pin_class=DTypes.Array, pin_type=Pin.PinType.DATA),
    ]
    output_pins = [
        NodeOutput(pin_type=Pin.PinType.EXEC),
        NodeOutput(pin_type=Pin.PinType.DATA, pin_name='索引', pin_class=DTypes.Integer),
        NodeOutput(pin_type=Pin.PinType.DATA, pin_name='元素', pin_class=DTypes.Class),
        NodeOutput(pin_type=Pin.PinType.EXEC, pin_name='完成'),
    ]

    def run_node(self):
        start = self.input(1)
        end = self.input(2) + 1
        step = self.input(3)
        for i in range(start, end, step):
            self._scene.get_view().new_session()
            self.output(1, i)
            self.output(2, self.input(4)[i])
            self.exec_output(0)
        self.exec_output(3)


class ForLoopNode(Node):
    pkg_name = '控制结构'
    node_title = 'For循环'
    node_description = '执行固定次数的循环'
    input_pins = [
        NodeInput(pin_type=Pin.PinType.EXEC),
        NodeInput(pin_name='开始', pin_class=DTypes.Integer, pin_type=Pin.PinType.DATA),
        NodeInput(pin_name='结束', pin_class=DTypes.Integer, pin_type=Pin.PinType.DATA),
        NodeInput(pin_name='步长', pin_class=DTypes.Integer, pin_type=Pin.PinType.DATA),
    ]
    output_pins = [
        NodeOutput(pin_type=Pin.PinType.EXEC, pin_name='循环体'),
        NodeOutput(pin_type=Pin.PinType.DATA, pin_name='索引', pin_class=DTypes.Integer),
        NodeOutput(pin_type=Pin.PinType.EXEC, pin_name='完成'),
    ]

    def run_node(self):
        start = self.input(1)
        end = self.input(2) + 1
        step = self.input(3)
        for i in range(start, end, step):
            self._scene.get_view().new_session()
            self.output(1, i)
            self.exec_output(0)
        self.exec_output(2)


class ForLoopWithBreakNode(Node):
    pkg_name = '控制结构'
    node_title = 'For循环(可跳出)'
    node_description = '执行固定次数的循环'
    input_pins = [
        NodeInput(pin_type=Pin.PinType.EXEC),
        NodeInput(pin_name='开始', pin_class=DTypes.Integer, pin_type=Pin.PinType.DATA),
        NodeInput(pin_name='结束', pin_class=DTypes.Integer, pin_type=Pin.PinType.DATA),
        NodeInput(pin_name='步长', pin_class=DTypes.Integer, pin_type=Pin.PinType.DATA),
        NodeInput(pin_name='跳出', pin_type=Pin.PinType.EXEC),
    ]
    output_pins = [
        NodeOutput(pin_type=Pin.PinType.EXEC, pin_name='循环体'),
        NodeOutput(pin_type=Pin.PinType.DATA, pin_name='索引', pin_class=DTypes.Integer),
        NodeOutput(pin_type=Pin.PinType.EXEC, pin_name='完成'),
    ]
    loop_break: bool = False

    def run_node(self):
        if self.exec_input(4):
            self.loop_break = True
            return
        start = self.input(1)
        end = self.input(2) + 1
        step = self.input(3)
        for i in range(start, end, step):
            if self.loop_break:
                break
            self._scene.get_view().new_session()
            self.output(1, i)
            self.exec_output(0)
        self.exec_output(2)


class WhileLoopNode(Node):
    pkg_name = '控制结构'
    node_title = 'While循环'
    node_description = '执行条件语句为真的循环'
    input_pins = [
        NodeInput(pin_type=Pin.PinType.EXEC),
        NodeInput(pin_name='条件', pin_class=DTypes.Boolean, pin_type=Pin.PinType.DATA),
    ]

    output_pins = [
        NodeOutput(pin_type=Pin.PinType.EXEC, pin_name='循环体'),
        NodeOutput(pin_type=Pin.PinType.EXEC, pin_name='完成'),
    ]

    def run_node(self):
        while input(1):
            self._scene.get_view().new_session()
            self.exec_output(0)
        self.exec_output(1)
