from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from Widgets.StyledWidget import StyledWidget
from Widgets.UpwardsComboBox import UpwardsComboBox

# >>> MODEL SELECTION >>>
class ModelSelection(StyledWidget):
    def __init__(self):
        super().__init__("ModelSelection")

        #Layout -V-
        layout = QVBoxLayout(self)

        # Styling
        self.setStyleSheet("""
            QWidget#ModelSelection {
                background-color: #000000;
            }
        """)

        # Width
        self.setFixedWidth(150)

        # Drop Down Box
        self.model_selection = UpwardsComboBox()
        self.model_selection.setObjectName("ModelSelectionBox")
        # Size
        self.model_selection.setFixedHeight(35)
        # Style
        self.model_selection.setStyleSheet("""
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

        # Add Widget
        layout.addWidget(self.model_selection)
    
    # Adds a List of models into the wodget for selection
    def add_models(self, models: list):

        # List of ollama models
        for model in models:
            self.model_selection.addItem(model)
# <<< MODEL SELECTION <<<
