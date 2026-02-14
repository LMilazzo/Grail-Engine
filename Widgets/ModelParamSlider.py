from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from Widgets.StyledWidget import StyledWidget

# >>> MODEL PARAMETER SLIDER >>>
class ModelParamSlider(StyledWidget):
    def __init__(self, default: float, width: int, title: QLabel, name: str, 
                 max=2.0, min=0.0, decimals=3, precision = 200.0, height = 150,
                 custom_scale = None, orientation=Qt.Orientation.Vertical):
        
        super().__init__("Container"+name)
        
        #--------------------------------------------------  
        #------------------ CORE LAYOUT ------------------- 
        #--------------------------------------------------

        layout = QVBoxLayout(self)

        # TITLE
        self.title = title

        # DECIMAL PLACES 
        self.decimals = decimals

        # Set Bounds
        self.min = min
        self.max = max
        self.precision = precision
        self.default = default

        #--------------------------------------------------  
        #------------------ VALUE LABEL ------------------- 
        #--------------------------------------------------

        # Value display label
        self.value_label = QLabel(f"{default:.{self.decimals}f}")

        #~~ ~~ ~~ ~~ ~~ ~~ ~~ STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.value_label.setStyleSheet("color: white;")

        #--------------------------------------------------  
        #--------------------- SLIDER --------------------- 
        #--------------------------------------------------

        self.slider = QSlider(orientation)
        self.slider.setObjectName(name)

        #--------------------------------------------------  
        #------------ EDIT SCALE/SET DEFAULTS -------------
        #--------------------------------------------------
    
        if custom_scale:
            self.custom_scale = custom_scale
            self.min = 0
            self.max = len(custom_scale) - 1
            self.stops = custom_scale
            self.precision = 1

            self.slider.setMinimum(int(self.min * self.precision)) # Min
            self.slider.setMaximum(int(self.max * self.precision)) # Max

        else:
            self.custom_scale = None
            self.slider.setMinimum(int(self.min * self.precision)) # Min
            self.slider.setMaximum(int(self.max * self.precision)) # Max

        self.slider.setValue(int(self.default * self.precision))
        self._update_label()

        
        #--------------------------------------------------  
        #--------------------- BUILD ----------------------
        #--------------------------------------------------

        layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.value_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.slider, alignment=Qt.AlignmentFlag.AlignHCenter)
        


        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.setStyleSheet(f"""
            QWidget#{"Container"+name} {{
                border: 1px solid #333333;
                border-radius: 12%
            }}
            QSlider#{name} {{
                background-color: #000000;
            }}
            QSlider#{name}::groove:vertical {{
                width: 6px;
                background: #222222;
                border: 1px solid #222222;
                border-radius: 3px;
            }}
            QSlider#{name}::handle:vertical {{
                background: #633636;
                border: 0px solid #aaaaaa;
                height: 10px;
                margin: 0 -5px;
                border-radius: 5px;
            }}
        """)

        # Sizing
        self.setFixedWidth(width)
        self.slider.setFixedWidth(int(width/2))
        self.setFixedHeight(height)
        self.setContentsMargins(0,0,0,0)
        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~

        # Connect slider move to label update
        self.slider.valueChanged.connect(self._update_label)

#__________________________________________________________________________________________________________

    #Updates the float label
    def _update_label(self):
        
        if self.custom_scale:

            self.value_label.setText(f"{self.getValue():.{self.decimals}f}")

            return
        
        self.value_label.setText(f"{self.getValue():.{self.decimals}f}")

    # returns the float value of the slider
    def getValue(self):

        if self.custom_scale:

            return self.custom_scale[int(self.slider.value())]
        
        #print(self.slider.value())

        return self.slider.value() / self.precision
    
    def setValue(self, value):

        self.slider.setValue(int(value * self.precision))

        self._update_label()

# <<< MODEL PARAMETER SLIDER <<<

