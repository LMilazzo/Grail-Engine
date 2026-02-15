from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt5.QtGui import QFont

from Model_Presets.Param_Presets import PARAM_PRESETS

from Widgets.StyledWidget import StyledWidget
from Widgets.CollapsibleLayout import CollapsibleLayout
from Widgets.CollapsibleWidget import CollapsibleWidget
from Widgets.SystemPromptInput import SystemPromptInput
from Widgets.WindowSpinBox import WindowSpinBox
from Widgets.ClearHistoryButton import ClearHistoryButton
from Widgets.ClearLastChatButton import ClearLastChatButton
from Widgets.ModelParamSlider import ModelParamSlider
from Widgets.ToolToggle import ToolToggle
from Widgets.PresetParamsButton import PresetParamsButton
from Widgets.PlotWindow import PlotWindow

import re

#**************  SIGNALS *****************
class WidgetSignals(QObject):
    clear_chat = pyqtSignal()
    clear_last_chats = pyqtSignal()
#**************  SIGNALS *****************

# >>> SIDE BAR >>>

WIDTH = 300
LABEL_STYLES = "color: white; padding: 0px; margin: 0px; font-weight: bold;"
TOKEN_SCALE = [16, 64, 128, 256, 512, 1024, 2048, 4096]

class SideBar(StyledWidget):
    def __init__(self):
        super().__init__("SideBarContainer")

        #**************  SIGNALS *****************
        self.signals =  WidgetSignals()

        #--------------------------------------------------  
        #--------------- SCROLL CONTAINER ----------------- 
        #--------------------------------------------------

        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("SideBarScrollArea")

        MASTER_layout = QVBoxLayout(self)
        MASTER_layout.addWidget(self.scroll_area)

        #~~ ~~ ~~ ~~ ~~ ~~ ~~ STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setContentsMargins(0,0,0,0)
        MASTER_layout.setSpacing(0)
        MASTER_layout.setContentsMargins(3,3,3,3)
        
        #Sidebar width
        self.setFixedWidth(WIDTH)
        #~~ ~~ ~~ ~~ ~~ ~~ ~~ STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~

        #--------------------------------------------------  
        #------------------ CORE LAYOUT ------------------- 
        #--------------------------------------------------
        self.main = StyledWidget("Sidebar")
        
        #Inner layout that is more important
        self.sidebar_layout = QVBoxLayout(self.main)

        # CONNECT THE MASTER content to the scroll area 
        self.scroll_area.setWidget(self.main)

        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.setStyleSheet("""
            QWidget#SideBarContainer {
                border: 1px solid white;
                border-radius: 10%;
                background-color: #000000;
            }
            QWidget#SideBarScrollArea{
                background-color: #000000;
                border: 0px solid green;
            }
            QWidget#Sidebar{
                border: 0px solid orange;
                background-color: transparent;
            }
        """)

        # Alignement
        self.sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~

#__________________________________________________________________________________________________________

        #--------------------------------------------------  
        #------------- SYSTEM PROMPT WIDGET --------------- 
        #--------------------------------------------------

        self.system_prompt_input = SystemPromptInput()

        self.system_prompt_input_collapsible = CollapsibleWidget("System Prompt", self.system_prompt_input)

        self.sidebar_layout.addWidget(self.system_prompt_input_collapsible)

#__________________________________________________________________________________________________________
        
        #--------------------------------------------------  
        #--------------- MEMORY OPTIONS ------------------- 
        #--------------------------------------------------

        # LAYOUT 
        # |  WINDOW SIZE    CLEAR CHAT    CLEAR LAST MESSAGES |
        
        self.memory_options_row = QHBoxLayout()

        self.memory_options_collapsible = CollapsibleLayout("Memory Options", self.memory_options_row)

        self.sidebar_layout.addWidget(self.memory_options_collapsible)

        #~~ ~~ ~~ ~~ ~~ ~~ ~~ STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.memory_options_row.setSpacing(3)

        #--------------------------------------------------  
        #------------ MESSAGE WINDOW SELECT ---------------
        #--------------------------------------------------

        self.memory_window_select = WindowSpinBox()

        memory_window_label = QLabel("Window: ")
        memory_window_label.setStyleSheet(LABEL_STYLES)

        # ADD LABEL THEN WIDGET
        self.memory_options_row.addWidget(memory_window_label)
        self.memory_options_row.addWidget(self.memory_window_select)

        # Add Manual spacing
        self.memory_options_row.addSpacing(7)

        #--------------------------------------------------  
        #------------ CLEAR ALL MEMORY WIDGET -------------
        #--------------------------------------------------
        
        self.clear_memory_btn = ClearHistoryButton()

        self.memory_options_row.addWidget(self.clear_memory_btn)
        
        # Add Manual spacing
        self.memory_options_row.addSpacing(7)

        self.clear_memory_btn.clicked.connect(self.signals.clear_chat.emit)

        #--------------------------------------------------  
        #---------- CLEAR LAST MSG/PAIR WIDGET ------------
        #--------------------------------------------------

        self.memory_clear_last_chats_btn = ClearLastChatButton()

        self.memory_options_row.addWidget(self.memory_clear_last_chats_btn)

        self.memory_clear_last_chats_btn.clicked.connect(self.signals.clear_last_chats.emit)
        
#__________________________________________________________________________________________________________
        
        #--------------------------------------------------  
        #--------------- MODEL PARAMETERS ----------------- 
        #--------------------------------------------------

        # Options: temperature, top_p, max_tokens, frequency_penalty, presence_penalty

        #--------------- CORE LAYOUT ----------------- 
        #
        #|--------------------------------|
        #|                                |
        #|   |-----|   |-----|  |-----|   |
        #|   |     |   |     |  |     |   |
        #|   |     |   |     |  |     |   |
        #|   |     |   |     |  |     |   |
        #|   |     |   |     |  |     |   |
        #|   |-----|   |-----|  |     |   |
        #|                      |     |   |
        #|                      |     |   |
        #|   |-----|   |-----|  |     |   |
        #|   |     |   |     |  |     |   |
        #|   |     |   |     |  |     |   |
        #|   |     |   |     |  |     |   |
        #|   |     |   |     |  |     |   |
        #|   |-----|   |-----|  |-----|   |
        #|                                |
        #|--------------------------------|

        self.params_main_layout = QHBoxLayout()

        self.params_right_column = QVBoxLayout()

        self.params_left_column = QVBoxLayout()

        self.params_left_column_row_1 = QHBoxLayout()
        self.params_left_column_row_2 = QHBoxLayout()

        # Add rows to left columns
        self.params_left_column.addLayout(self.params_left_column_row_1)
        self.params_left_column.addLayout(self.params_left_column_row_2)

        # Add Columns to Main layout in between two strectchs
        self.params_main_layout.addStretch()

        self.params_main_layout.addLayout(self.params_left_column)
        self.params_main_layout.addLayout(self.params_right_column)

        self.params_main_layout.addStretch()

        # Add main widget to the collapisble
        self.params_collapsible = CollapsibleLayout("Model Parameters", self.params_main_layout)

        self.sidebar_layout.addWidget(self.params_collapsible)

        #--------------------------------------------------  
        #--------------------- TEMP -----------------------
        #--------------------------------------------------

        # Make Label
        temp_lab = QLabel("Temp")
        temp_lab.setStyleSheet(LABEL_STYLES)
        
        self.temp_control = ModelParamSlider(
            min=0.0, max=2.0, default=0.9, width=70, 
            name="ModelTemp", title=temp_lab
        )

        self.params_left_column_row_1.addWidget(self.temp_control, alignment=Qt.AlignmentFlag.AlignLeft)

        #--------------------------------------------------  
        #--------------------- TOP P ----------------------
        #--------------------------------------------------

        # Make Label
        topP_lab = QLabel("Top P")
        topP_lab.setStyleSheet(LABEL_STYLES)        

        self.topP_control = ModelParamSlider(
            min=0.0, max=1.0, default=0.9, width=70, 
            name="ModelTopP", title=topP_lab
        )

        self.params_left_column_row_1.addWidget(self.topP_control, alignment=Qt.AlignmentFlag.AlignLeft)

        #--------------------------------------------------  
        #--------------------- Repeat ---------------------
        #--------------------------------------------------

        # Make Label
        repeat_lab = QLabel("Rep")
        repeat_lab.setStyleSheet(LABEL_STYLES)
      
        self.repeat_control = ModelParamSlider(
            min=1.0, max=2.0, default=1.1, width=70, 
            name="ModelRepeatPenalty", title=repeat_lab
        )

        self.params_left_column_row_2.addWidget(self.repeat_control, alignment=Qt.AlignmentFlag.AlignLeft)

        #--------------------------------------------------  
        #--------------------- Top K ----------------------
        #--------------------------------------------------

        # Make Label
        topK_lab = QLabel("Top K")
        topK_lab.setStyleSheet(LABEL_STYLES)
      
        self.topK_control = ModelParamSlider(
            min=0, max=100, default=40, width=70, precision=1, decimals=0,
            name="ModelTopK", title=topK_lab
        )
        self.params_left_column_row_2.addWidget(self.topK_control, alignment=Qt.AlignmentFlag.AlignLeft)

        #--------------------------------------------------  
        #--------------------- TOKENS ---------------------
        #--------------------------------------------------

        # Make Label
        tokens_lab = QLabel("Tokens")
        tokens_lab.setStyleSheet(LABEL_STYLES)

        self.token_control = ModelParamSlider(
            default=4, width=75, decimals=0, custom_scale=TOKEN_SCALE,
            name="ModelTokenLimit", title=tokens_lab, height=306
        )
        self.params_right_column.addWidget(self.token_control, alignment=Qt.AlignmentFlag.AlignHCenter)

#__________________________________________________________________________________________________________
        
        #--------------------------------------------------  
        #--------------- PARAMETERS PRESETS --------------- 
        #--------------------------------------------------

        # LAYOUT 

        # |--------------------|
        # |  (   default    )  |
        # |  (   default    )  |
        # |  (   default    )  |
        # |--------------------|

        self.presets_layout = QVBoxLayout()

        #~~ ~~ ~~ ~~ ~~ ~~ ~~ STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.presets_layout.setSpacing(5)
        self.presets_layout.setContentsMargins(1,1,1,1)

        self.presets_collapsible = CollapsibleLayout("Param Presets", self.presets_layout)
        
        self.sidebar_layout.addWidget(self.presets_collapsible)

        # This field is populated iteratively by the SideBar Method addPresets 


#__________________________________________________________________________________________________________
        
        #--------------------------------------------------  
        #--------------- TOOL ACTIVATIONS ----------------- 
        #--------------------------------------------------

        # LAYOUT 

        # |--------------------|
        # |  (   TOOL  [X]  )  |
        # |  (   TOOL  [ ]  )  |
        # |  (   TOOL  [X]  )  |
        # |--------------------|

        self.tool_activation_layout = QVBoxLayout()
                
        #~~ ~~ ~~ ~~ ~~ ~~ ~~ STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.tool_activation_layout.setSpacing(5)
        self.tool_activation_layout.setContentsMargins(1,1,1,1)

        self.tool_activation_collapsible = CollapsibleLayout("Toggle Tools", self.tool_activation_layout)

        self.sidebar_layout.addWidget(self.tool_activation_collapsible)

        # This field is populated iteratively by the SideBar Method addTools

#__________________________________________________________________________________________________________
        
        #--------------------------------------------------  
        #------------------ UMAP PLOT ---------------------
        #--------------------------------------------------

        self.plot_layout = QVBoxLayout()
        
        #~~ ~~ ~~ ~~ ~~ ~~ ~~ STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.plot_layout.setContentsMargins(1,1,1,1)

        self.plot_collapsible = CollapsibleLayout("Plot", self.plot_layout)

        self.sidebar_layout.addWidget(self.plot_collapsible)

        #The Plot object widget
        self.plot = PlotWindow(272)

        self.plot_layout.addWidget(self.plot)

#__________________________________________________________________________________________________________

        # Stretch
        self.sidebar_layout.addStretch()

#__________________________________________________________________________________________________________
    

# <<< SIDE BAR <<<