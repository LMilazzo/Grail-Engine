from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# >>> WINDOW SIZE SELECTION >>>
class WindowSpinBox(QSpinBox):
    def __init__(self):
        super().__init__()

        # Set Name
        self.setObjectName("WindowSizeSelection")

        #--------------------------------------------------  
        #------------------- VALUES ----------------------- 
        #--------------------------------------------------
        self.min = 0
        self.max = 99

        self.setRange(self.min, self.max)

        # DEFAULT VALUE
        self.setValue(12)

        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.setStyleSheet("""
            QSpinBox#WindowSizeSelection {
                border: 1px solid white;
                border-radius: 10%;
                background-color: #000000;
                color: white;
            }
            QSpinBox#WindowSizeSelection::up-button,
            QSpinBox#WindowSizeSelection::down-button {
                border: none;
                width: 0px;
            }
        """)

        # Size
        self.setFixedWidth(25)
        self.setFixedHeight(30)

        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~

# <<< WINDOW SIZE SELECTION <<<