from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from Widgets.StyledWidget import StyledWidget

# >>> TOOL TOGGLE >>>
class ToolToggle(StyledWidget):
    def __init__(self, name, title: QLabel):
        super().__init__("ToolToggleContainer"+name)

        self.status = False

        self.title = title

        self.checkbox = QCheckBox()
        self.checkbox.stateChanged.connect(self.update_status)
        self.checkbox.setObjectName("Toggle"+name)

        # Layout -H-
        layout = QHBoxLayout(self)

        self.setStyleSheet(f"""
            QWidget#{"ToolToggleContainer"+name} {{
                border: 1px solid #333333;
                border-radius: 12%
            }}
        """)
        
        # Add widgets
        layout.addWidget(self.title)
        layout.addWidget(self.checkbox)

        layout.addStretch()

        self.setFixedHeight(35)
    # Inverts the status of the checkbox
    def update_status(self):
        self.status = not self.status

    # Returns the check status
    def get_status(self):
        return self.status
# <<< TOOL TOGGLE <<<