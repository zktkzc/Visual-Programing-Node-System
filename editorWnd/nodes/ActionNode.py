from editorWnd.node import Node
from editorWnd.node_port import NodeOutput, NodeInput, Pin
from editorWnd.dtypes import DTypes


class BeginNode(Node):
    pkg_name = '默认行为'
    node_title = '开始运行'
    node_description = '开始节点（必须包含）'
    input_pins = []
    output_pins = [
        NodeOutput(pin_type=NodeOutput.PinType.EXEC, pin_name='开始')
    ]

    def run_node(self):
        self.exec_output(0)


class PrintNode(Node):
    pkg_name = '默认行为'
    node_title = '打印到控制台'
    node_description = '打印节点，输出到控制台'
    input_pins = [
        NodeInput(pin_type=Pin.PinType.EXEC),
        NodeInput(pin_type=Pin.PinType.DATA, pin_name='输入', pin_class=DTypes.String)
    ]
    output_pins = [
        NodeOutput(pin_type=Pin.PinType.EXEC),
        NodeOutput(pin_type=Pin.PinType.EXEC, pin_name='打印输出')
    ]

    def run_node(self):
        print(self.input_pins[0].get_pin_value())
