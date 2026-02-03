from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from Widgets.StyledWidget import StyledWidget

# >>> PRESET PARAMS BTN >>>
class PresetParamsButton(StyledWidget):
    def __init__(self, name, title, param_dict, callback=None):
        super().__init__("Preset"+name)

        # Name
        self.name = name

        # Preset
        self.params = param_dict

        # Callback
        self.callback = callback

        # The Button
        self.button = QPushButton(title)
        self.button.setObjectName("Preset"+name+"Button")
        self.button.setFixedHeight(30)
        self.button.setContentsMargins(0,0,0,0)

        # Click function
        if self.callback:
            self.button.clicked.connect(self._onclick)

        # Layout -H-
        layout = QHBoxLayout(self)

        self.setStyleSheet(f"""
            QWidget#{"Preset"+name} {{
            }}
            QPushButton#{"Preset"+name+"Button"} {{
                background-color: #000000;
                border: 1px solid #333333;
                border-radius: 12%;
                color: white;
                padding: 0px; 
                margin: 0px; 
                font-weight: bold;
            }}
        """)

        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        layout.addWidget(self.button)

    def _onclick(self):
        self.callback(self.params)
# <<< PRESET PARAMS BTN <<<
