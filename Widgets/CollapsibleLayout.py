from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# >>> COLLAPIBLE LAYOUT >>>
class CollapsibleLayout(QWidget):
    def __init__(self, title: str, content_layout: QLayout, parent=None):
        super().__init__(parent)

        # Wrap the layout in a QWidget
        self.content = QWidget()
        self.content.setLayout(content_layout)
        self.content.setVisible(False)  # start collapsed

        self.title = title

        self.active = False
        self.active_text = "+ " + self.title + " +"
        self.inactive_text = "- " + self.title + " -"

        # Toggle button
        self.toggle_btn = QPushButton()
        self.toggle_btn.setText(self.inactive_text)
        self.toggle_btn.setObjectName("toggle")
       
        self.toggle_btn.clicked.connect(self.toggle)

        # Styling
        self.toggle_btn.setFixedHeight(25)
        self.toggle_btn.setStyleSheet("""
            QPushButton#toggle {
                background-color: #000000;
                border: 1px solid white;
                border-radius: 10%;
                color: white;
                font-weight: bold;
            }
            QPushButton#toggle:hover{
                background-color: #191919;
            }
        """)

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        layout.addWidget(self.toggle_btn)
        layout.addWidget(self.content)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

    # toggles the section up or down
    def toggle(self):
        self.active = not self.active

        if self.active:
            self.toggle_btn.setText(self.active_text)
        else:
            self.toggle_btn.setText(self.inactive_text)

        self.content.setVisible(self.active)
# <<< COLLAPIBLE LAYOUT <<<