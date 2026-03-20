from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from pathlib import Path
import os

from Widgets.StyledWidget import StyledWidget

#**************  SIGNALS *****************
class WidgetSignals(QObject):
    delete_log = pyqtSignal(str)

#**************  SIGNALS *****************

# >>> LOG BUTTON >>>
LOGS_PATH = "HISTORY/LOGS/"

class LogButton(StyledWidget):
    def __init__(self, name, title):
        super().__init__("Log-"+name)

        #**************  SIGNALS *****************
        self.signals = WidgetSignals()

        #--------------------------------------------------  
        #------------------ CORE LAYOUT ------------------- 
        #--------------------------------------------------

        layout = QHBoxLayout(self)

        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self._setStyle(name)

        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.setFixedHeight(30)
        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~

        self.name = name

        #--------------------------------------------------  
        #---------------- PRESET BUTTON -------------------
        #--------------------------------------------------

        self.button = QPushButton(title)
        self.button.setObjectName("Log"+name+"Button")

        #~~ ~~ ~~ ~~ ~~ ~~ ~~ STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.button.setFixedHeight(30)
        self.button.setContentsMargins(0,0,0,0)

        self.button.clicked.connect(self._onclick)

        layout.addWidget(self.button)
        
        #--------------------------------------------------  
        #---------------- DELETE BUTTON -------------------
        #--------------------------------------------------

        self.rename_button = QPushButton()
        self.rename_button.setObjectName("renameButton")
        self.rename_button.setIcon(QIcon("Assets/SVG/Rename.svg"))
        self.rename_button.setIconSize(QSize(24, 24))
        self.rename_button.setToolTip("Rename")

        self.rename_button.clicked.connect(self._rename)
        
        #~~ ~~ ~~ ~~ ~~ ~~ ~~ STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.rename_button.setFixedWidth(25)
        self.rename_button.setFixedHeight(30)
        self.rename_button.setContentsMargins(0,0,0,0)

        layout.addWidget(self.rename_button)

        #--------------------------------------------------  
        #---------------- DELETE BUTTON -------------------
        #--------------------------------------------------

        self.dlt_button = QPushButton()
        self.dlt_button.setObjectName("dltButton")
        self.dlt_button.setIcon(QIcon("Assets/SVG/Close.svg"))
        self.dlt_button.setIconSize(QSize(16, 16))
        self.dlt_button.setToolTip("Delete")

        self.dlt_button.clicked.connect(self._delete)

        #~~ ~~ ~~ ~~ ~~ ~~ ~~ STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.dlt_button.setFixedWidth(25)
        self.dlt_button.setFixedHeight(30)
        self.dlt_button.setContentsMargins(0,0,0,0)

        layout.addWidget(self.dlt_button)

#__________________________________________________________________________________________________________

    def _onclick(self):
        print("Set conversation to ", self.name)
#__________________________________________________________________________________________________________

    def _rename(self):
        print("Rename Conversation", self.name)

        #--------------------------------------------------  
        #---------------- CREATE DIALOG -------------------
        #--------------------------------------------------
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Rename Conversation")
        dialog.setLabelText("Enter Name:")
        dialog.setTextValue(self.name)

        #~~ ~~ ~~ ~~ ~~ ~~ ~~ STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~
        dialog.setWindowIcon(QIcon("Assets/SVG/Rename.svg"))
        dialog.resize(300, 120)

        # show dialog and wait
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_name = dialog.textValue().strip()

            if not new_name:
                return

            # EXISTING NAMES
            names = [p.stem for p in Path("HISTORY/LOGS/").iterdir() if p.is_file()]
            if new_name in names:
                print("Cannot use")
                return

            # --- HANDLE NAME CHANGE ---
            print(f"Renaming '{self.name}' -> '{new_name}'")

            # SET OS NAME
            os.rename(LOGS_PATH+self.name+".jsonl", LOGS_PATH+new_name+".jsonl")

            # RESET UI NAME
            self.name = new_name
            self.button.setText(self.name)     
            self.button.setObjectName("Log"+new_name+"Button")

            # RESET OBJECT NAMES
            super().setName("Log-"+new_name)
            self._setStyle(new_name)


#__________________________________________________________________________________________________________

    def _delete(self): 
        print("Delete Conversation", self.objectName())

        # DELETE FROM UI SIGNAL
        self.signals.delete_log.emit(self.objectName())

        # DELETE FROM OS
        os.remove(LOGS_PATH+self.name+".jsonl")


#__________________________________________________________________________________________________________

    def _setStyle(self, name):
        
        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.setStyleSheet(f"""
            QWidget#{"Log-"+name} {{
                border: 1px solid #333333;
                border-radius: 12%;
            }}
            QPushButton#{"Log"+name+"Button"} {{
                background-color: #000000;
                border: 1px solid #333333;
                border-radius: 12%;
                color: white;
                padding: 0px; 
                margin: 0px; 
                font-weight: bold;
            }}
            QPushButton#{"Log"+name+"Button"}:hover {{
                background-color: #191919;
                border: 1px solid white;
            }}
            QPushButton#{"dltButton"} {{
                border: none;
            }}
            QPushButton#{"renameButton"} {{
                border: none;
            }}
        """)
# <<< LOG BUTTON <<<
