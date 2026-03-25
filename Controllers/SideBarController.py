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
import os

#**************  SIGNALS *****************
class ControllerSignals(QObject):
    no_logs = pyqtSignal()
    new_log_selected = pyqtSignal(str)
    reselect_from_rename = pyqtSignal(str)

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

        #--------------------------------------------------  
        #----------- REFERENCE LIST FOR LOGS  -------------
        #--------------------------------------------------
        self.LOG_REFERENCES = []
        self.last_auto_log = None
        self.ACTIVE_LOG = None

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

    #--------------------------------------------------  
    #------------------- LOG HANDLING -----------------
    #--------------------------------------------------
    def setLogs(self, logs: list):

        #EMPTY INCASE RESET
        clear_layout(self, self.SideBar.logs_left_column)
        clear_layout(self, self.SideBar.logs_right_column)
        self.LOG_REFERENCES.clear()

        left = True

        for l in logs:

            btn_name = l.replace(".jsonl", "")
            button = LogButton(btn_name, btn_name)

            # DELETE SIGNAL
            button.signals.delete_log.connect(self.deleteLog)

            # SELECTION SIGNALS
            button.signals.selected.connect(self.selectLog)

            # ADD TO REFERENCE LIST
            self.LOG_REFERENCES.append(button)

            # PICK COLUMN TO RENDER TO
            if left:
                self.SideBar.logs_left_column.addWidget(button, alignment=Qt.AlignmentFlag.AlignTop)
                left = not left
            else:
                self.SideBar.logs_right_column.addWidget(button, alignment=Qt.AlignmentFlag.AlignTop)
                left = not left
        
        # ADJUST COLUMNS
        self.SideBar.logs_left_column.addStretch()
        self.SideBar.logs_right_column.addStretch()

        # SELECT THE LAST AUTO LOG
        self.selectLog(self.last_auto_log)

    def deleteLog(self, button: StyledWidget, path: str, object_name: str):

        # DELETE FILE
        os.remove(path)

        # RECURSIVLY REMOVE FROM THE LAYOUT UI
        remove_widget_from_layout_rec(self.SideBar.logs_main_layout, object_name)

        #REMOVE FROM REFERENCE LIST
        self.LOG_REFERENCES.remove(button)

        # COUNT CURRENT LOGS AND EMIT SIGNAL IF A NEW ONE IS NEEDED
        if (self.SideBar.logs_right_column.count() + self.SideBar.logs_left_column.count()) < 3:
            self.signals.no_logs.emit()

        # IF THE CURRENT CHAT LOG IS DELETED SELECT ANOTHER
        elif button.selected:
            self.selectLog(self.LOG_REFERENCES[0].name)

    def selectLog(self, name: str, from_rename=False):
        for item in self.LOG_REFERENCES:

            # IF IT IS THE DESIRED ITEM SET IT ACTIVE AND EMIT SIGNALS
            if name == item.name or name == item.converted_name:
                item.changeStatus(override=True, status=True)
                self.ACTIVE_LOG = item.converted_name
                
                if not from_rename:
                    #Full signal
                    self.signals.new_log_selected.emit(self.ACTIVE_LOG)
                else:
                    self.signals.reselect_from_rename.emit(self.ACTIVE_LOG)

            # OTHERWISE DEACTIVE
            else:
                item.changeStatus(override=True, status=False)

    def autoSelectLog(self, name: str):
        print("Auto selecting ", name)
        self.last_auto_log = name
#__________________________________________________________________________________________________________

    def getPromptRelevantData(self):

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