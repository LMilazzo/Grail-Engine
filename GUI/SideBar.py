from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt5.QtGui import QFont

from Model_Presets.Param_Presets import PARAM_PRESETS

from Controllers.ChatController import *

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

import re

# >>> SIDE BAR >>>
class SideBar(StyledWidget):
    def __init__(self):
        super().__init__("SideBarContainer")
        
        # A registry of tool names and their toggle switches 
        self.active_tools = {}

        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("SideBarScrollArea")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setContentsMargins(0,0,0,0)

        # Internal Sidebar
        self.content = StyledWidget("Sidebar")
        self.content.setContentsMargins(0,0,0,0)
        self._layout = QVBoxLayout(self.content)

        # Set as content widget
        self.scroll_area.setWidget(self.content)

        #Container Layout -V-
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.scroll_area)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(3,3,3,3)

        # Styling
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
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # OPTIONS LABELS STYLE
        self._label_styles = "color: white; padding: 0px; margin: 0px; font-weight: bold;"

        #------------------------------------------------------------------------------------
        # Add System Prompt Area

        self.system_prompt_input = SystemPromptInput()
        self.spi_wrapper = CollapsibleWidget("System Prompt", self.system_prompt_input)
        self._layout.addWidget(self.spi_wrapper)

        #------------------------------------------------------------------------------------
        # Add memory options

        # Column layout
        self.mem_options_col = QVBoxLayout()

        #Top horizontal GOAL: |   WIPE_BTN     WINDOW SIZE |
        self.mem_options_row1 = QHBoxLayout()
        self.mem_options_row1.setSpacing(3)

        # Window Size Selection
        mem_window_label = QLabel("Window: ")
        mem_window_label.setStyleSheet(self._label_styles)
        self.mem_options_row1.addWidget(mem_window_label)
        self.memory_window_selection = WindowSpinBox()
        self.mem_options_row1.addWidget(self.memory_window_selection)
        self.mem_options_row1.addSpacing(15)

        # Memory wipe button
        self.memory_wipe_btn = ClearHistoryButton()
        self.mem_options_row1.addWidget(self.memory_wipe_btn)
        self.mem_options_row1.addStretch()

        # Create row 2
        self.mem_options_row2 = QHBoxLayout()
        self.mem_options_row2.setSpacing(3)
        self.mem_clear_last_chat_btn = ClearLastChatButton()
        self.mem_options_row2.addWidget(self.mem_clear_last_chat_btn)
        self.mem_options_row2.addStretch()

        #Add rows to col
        self.mem_options_col.addLayout(self.mem_options_row1)
        self.mem_options_col.addLayout(self.mem_options_row2)

        self.mem_opt_wrapper = CollapsibleLayout("Memory Options", self.mem_options_col)

        self._layout.addWidget(self.mem_opt_wrapper)

        #------------------------------------------------------------------------------------
        # Add model parameter options
        # Options: temperature, top_p, max_tokens, frequency_penalty, presence_penalty

        # Define Columns
        self.model_params_col1 = QVBoxLayout()
        self.model_params_col1.setContentsMargins(0,0,0,0)
        self.model_params_col2 = QVBoxLayout()
        self.model_params_col2.setContentsMargins(0,0,0,0)

        # Define rows
        self.model_params_row1 = QHBoxLayout()
        self.model_params_row1.setContentsMargins(0,0,0,0)
        self.model_params_row2 = QHBoxLayout()
        self.model_params_row2.setContentsMargins(0,0,0,0)

        # Make Labels
        temp_lab = QLabel("Temp")
        topP_lab = QLabel("Top P")
        tokens_lab = QLabel("Tokens")
        repeat_lab = QLabel("Rep")
        topK_lab = QLabel("Top K")
        temp_lab.setStyleSheet(self._label_styles)
        topP_lab.setStyleSheet(self._label_styles)
        tokens_lab.setStyleSheet(self._label_styles)
        repeat_lab.setStyleSheet(self._label_styles)
        topK_lab.setStyleSheet(self._label_styles)

        # Define widgets
        # Temp
        self.temp_control = ModelParamSlider(
            min=0.0, max=2.0, default=0.9, width=53, 
            name="ModelTemp", title=temp_lab
        )
        self.model_params_row1.addWidget(self.temp_control, alignment=Qt.AlignmentFlag.AlignLeft)
        # Top P
        self.topP_control = ModelParamSlider(
            min=0.0, max=1.0, default=0.9, width=53, 
            name="ModelTopP", title=topP_lab
        )
        self.model_params_row1.addWidget(self.topP_control, alignment=Qt.AlignmentFlag.AlignLeft)
        # Repeat Penalty
        self.repeat_control = ModelParamSlider(
            min=1.0, max=2.0, default=1.1, width=53, 
            name="ModelRepeatPenalty", title=repeat_lab
        )
        self.model_params_row2.addWidget(self.repeat_control, alignment=Qt.AlignmentFlag.AlignLeft)
        # Top K control
        self.topK_control = ModelParamSlider(
            min=0, max=100, default=40, width=53, precision=1, decimals=0,
            name="ModelTopK", title=topK_lab
        )
        self.model_params_row2.addWidget(self.topK_control, alignment=Qt.AlignmentFlag.AlignLeft)

        # Add rows to col 1
        self.model_params_col1.addLayout(self.model_params_row1)
        self.model_params_col1.addLayout(self.model_params_row2)

        # Create token limit widget and add to col 2
        # Token Limit
        self.token_control = ModelParamSlider(
            default=4, width=57, decimals=0, custom_scale=[16, 64, 128, 256, 512, 1024, 2048, 4096],
            name="ModelTokenLimit", title=tokens_lab, height=306
        )
        self.model_params_col2.addWidget(self.token_control, alignment=Qt.AlignmentFlag.AlignHCenter)


        # Add Cols to vertical layout
        self.model_params_layout = QHBoxLayout()
        self.model_params_layout.addLayout(self.model_params_col1)
        self.model_params_layout.addLayout(self.model_params_col2)
        self.model_params_layout.addStretch()

        self.model_params_wrapper = CollapsibleLayout("Model Parameters", self.model_params_layout)

        self._layout.addWidget(self.model_params_wrapper)

        #------------------------------------------------------------------------------------

        # A section that contains quick preset buttons for model parameters

        self.param_presets_layout = QVBoxLayout()
        self.param_presets_layout.setSpacing(5)
        self.param_presets_layout.setContentsMargins(1,1,1,1)
        self.param_presets_wrapper = CollapsibleLayout("Param Presets", self.param_presets_layout)
        
        # A Dictionary to hold the iteratively generated buttons
        self.param_presets = {}

        # Make a button for each preset
        for preset_key, preset in PARAM_PRESETS.items():
            btn = PresetParamsButton(preset_key.replace(" ", ""), preset_key, 
                                     preset, callback=self.activatePreset)
            self.param_presets[preset_key] = btn
            self.param_presets_layout.addWidget(btn)

        self._layout.addWidget(self.param_presets_wrapper)

        #------------------------------------------------------------------------------------

        # A section to toggle on and off certain tool functions
        self.tool_toggles_layout = QVBoxLayout()
        self.tool_toggles_layout.setSpacing(5)
        self.tool_toggles_layout.setContentsMargins(1,1,1,1)
        self.tool_wrapper = CollapsibleLayout("Toggle Tools", self.tool_toggles_layout)
        self._layout.addWidget(self.tool_wrapper)

        #------------------------------------------------------------------------------------

        # Stretch
        self._layout.addStretch()

        # Fixed Width
        self.setFixedWidth(220)

    # Assigns a controller to this sidebar to access prompt settings
    def setChatController(self, controller: ChatController):

        # Set Controller
        self.chat_controller = controller

        # Connect options buttons to controller methods
        #Memory wipe
        self.memory_wipe_btn.clicked.connect(self.chat_controller.clearMemory)
        #Window change
        self.memory_window_selection.valueChanged.connect(self.chat_controller.updateWindowSize)
        #Clear last message
        self.mem_clear_last_chat_btn.clicked.connect(self.chat_controller.undo)
    
        # Populate the tools list
        self.addToolToggles(self.chat_controller, self.chat_controller.getTools())

    # Refractors the Tools drop down and populates it with available content from ChatController
    def addToolToggles(self, chat_controller: ChatController, registry_names: list):

        reference_dict = {}

        for tool in registry_names:

            # Add Tool toggle to sidebar
            title = QLabel(tool)
            title.setStyleSheet(self._label_styles)
            toggle = ToolToggle(
                re.sub(r'[^a-zA-Z0-9]', '', tool),  #Clean title to add as object name
                title
            )
            self.tool_toggles_layout.addWidget(toggle)

            # Add Title and object reference to dictionary
            reference_dict[tool] = toggle

        # Finish sidebar element with stretch        
        self.tool_toggles_layout.addStretch()

        # Set ChatControllers reference dictionary to the toggle switches
        chat_controller.setToolToggleRefrences(reference_dict)

    # Sets the 4 core model parameters according to a preset.
    def activatePreset(self, param_dict: dict):
        self.temp_control.set_value(param_dict["temp"])
        self.topP_control.set_value(param_dict["topP"])
        self.topK_control.set_value(param_dict["topK"])
        self.repeat_control.set_value(param_dict["repeat_penalty"])
# <<< SIDE BAR <<<