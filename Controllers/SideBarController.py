from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import QHBoxLayout

from GUI.SideBar import SideBar, LABEL_STYLES
from Widgets.PresetParamsButton import PresetParamsButton
from Widgets.ToolToggle import ToolToggle
from Widgets.LogButton import LogButton
from Widgets.StyledWidget import StyledWidget

from Utils.PyQt_Utils import remove_widget_from_layout_rec, clear_layout

import re

#**************  SIGNALS *****************
class ControllerSignals(QObject):
    pass

#**************  SIGNALS *****************

# >>> SIDEBAR CONTROLLER >>>
class SideBarController():
    def __init__(self, SideBar: SideBar):

        #**************  SIGNALS *****************
        self.signals = ControllerSignals()

        #--------------------------------------------------  
        #------------------- UI OBJECTS -------------------
        #--------------------------------------------------
        self.SideBar = SideBar

        #--------------------------------------------------  
        #----------- REFERENCE DICT FOR TOOLS -------------
        #--------------------------------------------------
        # A LIST OF TOOL TOGGLE OBJECT TO REFRENCE TO FIND THE ACTIVATED ONES
        self.TOOL_REFERENCE_DICT = {}

#__________________________________________________________________________________________________________

    #--------------------------------------------------  
    #------------------- UI UPDATES -------------------
    #--------------------------------------------------

    def addPresets(self, preset_dict: dict):
        for key, preset in preset_dict.items():
            button = PresetParamsButton(key.replace(" ", ""), key, preset, callback=self.applyPreset)

            self.SideBar.presets_layout.addWidget(button)

    def addTools(self, tool_list: list):

        for tool in tool_list:

            # Create Label
            title = QLabel(tool)
            title.setStyleSheet(LABEL_STYLES)
            toggle = ToolToggle(
                re.sub(r'[^a-zA-Z0-9]', '', tool),  #Clean title to add as object name
                title
            )

            self.SideBar.tool_activation_layout.addWidget(toggle)
            
            self.TOOL_REFERENCE_DICT[tool] = toggle

    def setPlot(self, html):
        self.SideBar.plot.setHtml(html)

    def setLogs(self, logs: list):
        
        #EMPTY INCASE RESET
        clear_layout(self, self.SideBar.logs_left_column)
        clear_layout(self, self.SideBar.logs_right_column)

        left = True

        for l in logs:

            btn_name = l.replace(".jsonl", "")
            button = LogButton(btn_name, btn_name)
            button.signals.delete_log.connect(self.deleteLog)

            if left:
                self.SideBar.logs_left_column.addWidget(button, alignment=Qt.AlignmentFlag.AlignTop)
                left = not left
            else:
                self.SideBar.logs_right_column.addWidget(button, alignment=Qt.AlignmentFlag.AlignTop)
                left = not left
        
        self.SideBar.logs_left_column.addStretch()
        self.SideBar.logs_right_column.addStretch()

    def deleteLog(self, object_name: str):

        # RECURSIVLY REMOVE FROM THE LAYOUT UI
        remove_widget_from_layout_rec(self.SideBar.logs_main_layout, object_name)

#__________________________________________________________________________________________________________

    def getPromptRelavantData(self):

        return {
            "system" : self.SideBar.system_prompt_input.getText(),
            "temp" : self.SideBar.temp_control.getValue(),
            "topP" : self.SideBar.topP_control.getValue(),
            "topK" : self.SideBar.topK_control.getValue(),
            "rep" : self.SideBar.repeat_control.getValue(),
            "tokens" : self.SideBar.token_control.getValue(),
            "tools" : self.getSelectedTools()
        }

    def getSelectedTools(self):

        active = []

        for key, value in self.TOOL_REFERENCE_DICT.items():
            if value.getStatus():
                active.append(key)
        return active

        #Applies a selected preset
    
    def applyPreset(self, preset_values: dict):

        self.SideBar.temp_control.setValue(preset_values["temp"])
        self.SideBar.topP_control.setValue(preset_values["topP"])
        self.SideBar.topK_control.setValue(preset_values["topK"])
        self.SideBar.repeat_control.setValue(preset_values["repeat_penalty"])

# <<< SIDEBAR CONTROLLER <<<