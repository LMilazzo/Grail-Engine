from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from Widgets.StyledWidget import StyledWidget
from Widgets.UpwardsComboBox import UpwardsComboBox

# >>> MODEL SELECTION >>>
class ModelSelection(StyledWidget):
    def __init__(self):
        super().__init__("ModelSelection")

        #--------------------------------------------------  
        #------------------ CORE LAYOUT ------------------- 
        #--------------------------------------------------

        layout = QVBoxLayout(self)

        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.setStyleSheet("""
            QWidget#ModelSelection {
                background-color: #000000;
            }
        """)

        # Width
        self.setFixedWidth(150)
        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~

        #--------------------------------------------------  
        #------------- MODEL SELECTION WIDGET -------------
        #--------------------------------------------------

        self.select_box = UpwardsComboBox()

        self.select_box.setObjectName("ModelSelectionBox")

        #~~ ~~ ~~ ~~ ~~ ~~ ~~ STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~
        # Style
        self.select_box.setStyleSheet("""
            QComboBox#ModelSelectionBox {
                background-color: #000000;
                color: white;
                border: 1px solid white;
                border-radius: 10%;
            }
            QComboBox#ModelSelectionBox::drop-down{
                border: none;
                width: 0px;
            }
        """)
        
        # Size
        self.select_box.setFixedHeight(35)
        #~~ ~~ ~~ ~~ ~~ ~~ ~~ STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~

        layout.addWidget(self.select_box)
#__________________________________________________________________________________________________________

    # Adds a List of models into the widget for selection
    def addModels(self, models: list):

        # List of ollama models
        for model in models:
            self.select_box.addItem(model)
            
# <<< MODEL SELECTION <<<
