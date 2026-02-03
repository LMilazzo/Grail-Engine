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

        # Toggle button
        self.toggle_btn = QToolButton()
        self.toggle_btn.setText(title)
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setChecked(False)
        self.toggle_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toggle_btn.setArrowType(Qt.ArrowType.RightArrow)
        self.toggle_btn.clicked.connect(self.toggle)

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        layout.addWidget(self.toggle_btn)
        layout.addWidget(self.content)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        # Styling
        self.setStyleSheet("""
            QToolButton {
                border: 1px solid white;
                border-radius: 10%;
                color: white;
                font-weight: bold;
                text-align: left;
            }
            QToolButton::menu-indicator {
                image: none;
            }
        """)

    # toggles the section up or down
    def toggle(self):
        expanded = self.toggle_btn.isChecked()
        self.content.setVisible(expanded)
        self.toggle_btn.setArrowType(Qt.ArrowType.DownArrow if expanded else Qt.ArrowType.RightArrow)
# <<< COLLAPIBLE LAYOUT <<<