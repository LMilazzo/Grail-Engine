from PyQt6.QtWidgets import *

from GUI.SideBar import SideBar
from GUI.ChatArea import ChatArea
from GUI.PromptArea import PromptArea

from Controllers.DataLoader import DataLoader
from Controllers.AppMediator import AppMediator

# >>> MAIN WINDOW >>>
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 600

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

#__________________________________________________________________________________________________________

        #--------------------------------------------------  
        #------------- BUILD UI CORE ELEMENTS ------------- 
        #--------------------------------------------------  

        # Window Title
        self.setWindowTitle("--- Ollama Chat App ---")
        
        # Window Size
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Set Name
        self.setObjectName("MainWindow")

        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.setStyleSheet("""
            QMainWindow#MainWindow {
                background-color: #000000;
            }
        """)
        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~

        # Central Widget
        central = QWidget()
        self.setCentralWidget(central)
        
        #--------------------------------------------------  
        #------------------ CORE LAYOUT ------------------- 
        #--------------------------------------------------
        
        #    left col       right col
        # |-----------|--------------------|
        # |           |                    |
        # |           |                    |
        # |           |         1          |   right col row top
        # |     3     |                    |
        # |           |                    |
        # |           |--------------------|
        # |           |                    |   right col row bottom
        # |           |         2          |
        # |-----------|--------------------|

        self.left_column = QVBoxLayout()

        self.right_column = QVBoxLayout()
        self.right_column.setSpacing(0)

        self.right_column_row_top = QHBoxLayout()
        self.right_column.addLayout(self.right_column_row_top)

        self.right_column_row_bottom = QHBoxLayout()
        self.right_column.addLayout(self.right_column_row_bottom)

        MASTER_layout = QHBoxLayout(central)
        MASTER_layout.setContentsMargins(3,3,3,3)

        MASTER_layout.addLayout(self.left_column)
        MASTER_layout.addLayout(self.right_column)

        #--------------------------------------------------  
        #-------------------- SIDE BAR -------------------- 
        #--------------------------------------------------

        self._SIDEBAR = SideBar()
        self.left_column.addWidget(self._SIDEBAR)


        #--------------------------------------------------  
        #-------------------- CHAT AREA ------------------- 
        #--------------------------------------------------

        self._CHAT_AREA = ChatArea()
        self.right_column_row_top.addWidget(self._CHAT_AREA)

        #--------------------------------------------------  
        #------------------- PROMP AREA ------------------- 
        #--------------------------------------------------

        self._PROMPT_AREA = PromptArea()
        self.right_column_row_bottom.addWidget(self._PROMPT_AREA)
        
#__________________________________________________________________________________________________________

        #--------------------------------------------------  
        #------------------- DATA LOADER ------------------ 
        #--------------------------------------------------
        self._DATALOADER = DataLoader()


        #--------------------------------------------------  
        #------------------- APP MEDIATOR ----------------- 
        #--------------------------------------------------
        self._APP_MEDIATOR = AppMediator(self._PROMPT_AREA, self._CHAT_AREA, self._SIDEBAR, self._DATALOADER)


# <<< MAIN WINDOW <<<