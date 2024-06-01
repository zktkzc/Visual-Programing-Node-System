from PySide6.QtWidgets import QCheckBox, QLineEdit


class DTypes:
    # 数据类型
    Integer = 'int'
    Float = 'float'
    String = 'str'
    Array = 'list'
    Boolean = 'bool'
    Dict = 'dict'
    Class = 'class'
    Vector = 'vector'

    Color_Map = {
        'float': '#2fff09',
        'int': '#22ee90',
        'str': '#ee0ba0',
        'list': '#d4aa24',
        'bool': '#cc0606',
        'dict': '#ed6c03',
        'class': '#0747bb',
        'vector': '#055c54'
    }

    default_widget = {
        'int': QLineEdit,
        'bool': QCheckBox,
        'str': QLineEdit,
        'float': QLineEdit,
        'list': QLineEdit,
        'dict': QLineEdit,
        'class': QLineEdit,
        'vector': QLineEdit
    }


