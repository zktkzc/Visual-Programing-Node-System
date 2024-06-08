'''
editor的一些可设置的参数
'''


class EditorConfig:
    EDITOR_SCENE_BACKGROUND_COLOR = '#212121'
    EDITOR_SCENE_GRID_NORMAL_LINE_COLOR = '#313131'
    EDITOR_SCENE_GRID_DARK_LINE_COLOR = '#151515'

    EDITOR_SCENE_GRID_NORMAL_LINE_WIDTH = 1.0
    EDITOR_SCENE_GRID_DARK_LINE_WIDTH = 1.5

    EDITOR_SCENE_GRID_SIZE = 20
    EDITOR_SCENE_GRID_CHUNK = 10

    EDITOR_SCENE_WIDTH = 32000
    EDITOR_SCENE_HEIGHT = 32000

    EDITOR_NODE_TITLE_FONT_SIZE = 14
    EDITOR_NODE_TITLE_FONT = 'Microsoft YaHei'
    EDITOR_NODE_PIN_LABEL_FONT_SIZE = 12
    EDITOR_NODE_PIN_LABEL_FONT = 'Microsoft YaHei'


class NodeConfig:
    PORT_ICON_SIZE = 20
    NODE_RADIUS = 1
    node_title_background_color = {
        '默认行为': '#f5232e',
        '基本运算': '#88df00',
        '节点转换': '#fa8b17',
        '控制结构': '#4e90fe',
        '输入节点': '#00bfff',
    }


class GroupConfig:
    GROUP_TITLE_BACKGROUND_COLOR = '#213252'
    GROUP_TITLE_COLOR = '#aaaaaa'
    GROUP_CONTENT_BACKGROUND_COLOR = '#888888'
    GROUP_TITLE_FONT_SIZE = 14
    GROUP_TITLE_FONT = 'Microsoft YaHei'
    GROUP_RADIUS = 1
