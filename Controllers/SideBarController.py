from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import QHBoxLayout

from GUI.SideBar import SideBar, LABEL_STYLES
from Widgets.PresetParamsButton import PresetParamsButton
from Widgets.ToolToggle import ToolToggle

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