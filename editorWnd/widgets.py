from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import Qt


class NodeListWidget(QTreeWidget):
    def __init__(self, data: dict, parent=None):
        '''
        data = {
            'package name': [
                'node title': Nodecls,
            ]
        }
        :param data:
        :param parent:
        '''
        super().__init__(parent)
        self.resize(200, 300)
        self.setColumnCount(1)
        self.setHeaderHidden(True)

        self.data = data
        self.construct_tree()

    def construct_tree(self, filter=None):
        self.clear()
        items = []
        for pkg_name in self.data.keys():
            item = QTreeWidgetItem([pkg_name])
            for node_title in self.data[pkg_name].keys():
                node_item = QTreeWidgetItem([node_title])
                # node_item.setData(0, Qt.ItemDataRole.UserRole, self.data[pkg_name][node_title])
                item.addChild(node_item)
            items.append(item)
        self.insertTopLevelItems(0, items)
