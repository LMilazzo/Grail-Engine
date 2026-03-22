from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from pathlib import Path
import os

from Widgets.StyledWidget import StyledWidget

#**************  SIGNALS *****************
class WidgetSignals(QObject):
    delete_log = pyqtSignal(StyledWidget, str, str)
    selected = pyqtSignal(str)
    selected_name_changed = pyqtSignal(str)

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
        
        self.name = name.replace("_", " ")
        self.converted_name = name.replace(" ", "_")

        self.selected = False

        #--------------------------------------------------  
        #---------------- PRESET BUTTON -------------------
        #--------------------------------------------------

        self.button = QPushButton()
        self.button.setObjectName("Log"+name+"Button")
        self.button.setToolTip(self.name)

        # SET BUTTON TEXT
        font_metrics = QFontMetrics(self.button.font())
        elided_text = font_metrics.elidedText(self.name, Qt.TextElideMode.ElideRight, 72)
        self.button.setText(elided_text)

        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self._setStyle(name)

        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        
        self.setFixedHeight(30)
        self.setFixedWidth(126)
        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~

        #~~ ~~ ~~ ~~ ~~ ~~ ~~ STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.button.setFixedHeight(30)
        self.button.setFixedWidth(75)
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

        self.signals.selected.emit(self.name)
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

            new_converted = new_name.replace(" ", "_")

            # SET OS NAME
            os.rename(LOGS_PATH+self.converted_name+".jsonl", LOGS_PATH+new_converted+".jsonl")

            # RESET UI NAME
            self.name = new_name
            self.converted_name = new_converted
   
            self.button.setObjectName("Log"+self.converted_name+"Button")
            self.button.setToolTip(self.name)

            # SET BUTTON TEXT
            font_metrics = QFontMetrics(self.button.font())
            elided_text = font_metrics.elidedText(self.name, Qt.TextElideMode.ElideRight, 72)
            self.button.setText(elided_text)

            # RESET OBJECT NAMES
            super().setName("Log-"+self.converted_name)
            self._setStyle(self.converted_name)

            if self.selected:
                self.signals.selected_name_changed.emit(self.converted_name)

#__________________________________________________________________________________________________________

    def _delete(self): 
        
        path = LOGS_PATH+self.converted_name+".jsonl"

        # DELETE FROM UI SIGNAL
        self.signals.delete_log.emit(self, path, self.objectName())

#__________________________________________________________________________________________________________

    def _setStyle(self, name):
        
        self.update()

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

    def paintEvent(self, event):
        # draw normal button first
        super().paintEvent(event)

        if not self.selected:
            self.button.setFixedHeight(30)
            self.button.setFixedWidth(75)
            return
        self.button.setFixedHeight(26)
        self.button.setFixedWidth(70)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        base_color = QColor("#d3b6d8")

        rect = self.rect()

        # draw layered glow
        for i in range(1, 2):
            color = QColor(base_color)
            color.setAlpha(150 - i * 25)  # fade out

            pen = QPen(color)
            pen.setWidth(2 + i)

            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)

            painter.drawRoundedRect(
                rect.adjusted(i, i, -i, -i), 12, 12
            )
#__________________________________________________________________________________________________________

    def changeStatus(self, override=False, status=False):

        if override: 
            self.selected = status
        else:
            self.selected = not self.selected

        self._setStyle(self.converted_name)
# <<< LOG BUTTON <<<
