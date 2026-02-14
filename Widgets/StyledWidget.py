from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# >>> STYLED WIDGET >>>
class StyledWidget(QWidget):
    def __init__(self, object_name: str, parent=None):
        super().__init__(parent)

        self.setObjectName(object_name)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

# <<< STYLED WIDGET <<<