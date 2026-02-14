from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from Widgets.StyledWidget import StyledWidget

# >>> PRESET PARAMS BTN >>>
class PresetParamsButton(StyledWidget):
    def __init__(self, name, title, param_dict, callback=None):
        super().__init__("Preset"+name)

        #--------------------------------------------------  
        #------------------ CORE LAYOUT ------------------- 
        #--------------------------------------------------

        layout = QHBoxLayout(self)

        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~
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
            QPushButton#{"Preset"+name+"Button"}:hover {{
                background-color: #191919;
                border: 1px solid white;
            }}
        """)

        
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~

        self.name = name

        # Preset Dict
        self.params = param_dict

        # Callback
        self.callback = callback

        #--------------------------------------------------  
        #---------------- PRESET BUTTON -------------------
        #--------------------------------------------------

        self.button = QPushButton(title)
        self.button.setObjectName("Preset"+name+"Button")

        #~~ ~~ ~~ ~~ ~~ ~~ ~~ STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.button.setFixedHeight(30)
        self.button.setContentsMargins(0,0,0,0)

        # Click function
        if self.callback:
            self.button.clicked.connect(self._onclick)

        layout.addWidget(self.button)

    def _onclick(self):
        self.callback(self.params)
# <<< PRESET PARAMS BTN <<<
