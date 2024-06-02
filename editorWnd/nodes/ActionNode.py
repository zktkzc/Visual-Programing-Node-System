from editorWnd.node import Node
from editorWnd.node_port import NodeOutput


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
