from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout

from Controllers.ChatController import *

from GUI.SideBar import SideBar
from GUI.ChatArea import ChatArea

# >>> MAIN WINDOW >>>
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window Title
        self.setWindowTitle("--- Ollama Chat App ---")
        
        # Window Size
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Set Name
        self.setObjectName("MainWindow")

        # Styling
        self.setStyleSheet("""
            QMainWindow#MainWindow {
                background-color: #000000;
            }
        """)

        # Central Widget
        central = QWidget()
        self.setCentralWidget(central)

        # Layout -H-
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(3,3,3,3)

        # SideBar Element
        self.sidebar = SideBar()
        main_layout.addWidget(self.sidebar)

        # Chat Area Element
        self.chat_area = ChatArea()
        main_layout.addWidget(self.chat_area)

        # Chat Controller
        self.chat_controller = ChatController(
            self.chat_area, 
            self.sidebar
        )
        
        # Set Controllers
        self.chat_area.setChatController(self.chat_controller)     
        self.sidebar.setChatController(self.chat_controller)   
# <<< MAIN WINDOW <<<