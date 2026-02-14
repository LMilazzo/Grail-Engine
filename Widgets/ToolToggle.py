from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from Widgets.StyledWidget import StyledWidget

# >>> TOOL TOGGLE >>>
class ToolToggle(StyledWidget):
    def __init__(self, name, title: QLabel):
        super().__init__("ToolToggleContainer"+name)

        #--------------------------------------------------  
        #------------------ CORE LAYOUT ------------------- 
        #--------------------------------------------------

        layout = QHBoxLayout(self)

        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.setStyleSheet(f"""
            QWidget#{"ToolToggleContainer"+name} {{
                border: 1px solid #333333;
                border-radius: 12%
            }}
        """)

        self.setFixedHeight(40)
        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~

        # DEFAULT STATUS
        self.status = False

        # TITLE
        self.title = title

        #--------------------------------------------------  
        #--------------- CHECKBOX WIDGET ------------------ 
        #--------------------------------------------------
        self.checkbox = QCheckBox()
        
        self.checkbox.setObjectName("Toggle"+name)

        # mAKE A CONNECTION BETWEEN STATUS UPDATE AND CHECKING
        self.checkbox.stateChanged.connect(self.update_status)

        # Add widgets
        layout.addWidget(self.title)
        layout.addWidget(self.checkbox)

        layout.addStretch()

#__________________________________________________________________________________________________________

    # Inverts the status of the checkbox
    def update_status(self):
        self.status = not self.status

    # Returns the check status
    def getStatus(self):
        return self.status
# <<< TOOL TOGGLE <<<