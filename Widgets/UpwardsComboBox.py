from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# >>> UPWARDS COMBO BOX >>>
# A combo box implementation that displays objects
# above the original box position
class UpwardsComboBox(QComboBox):
    popupAboutToBeShown = pyqtSignal()

    def showPopup(self):
        self.popupAboutToBeShown.emit()

        super().showPopup()

        popup = self.findChild(QFrame)
        if not popup:
            return

        popup.hide()

        def reposition():
            popup.move(
                popup.x(),
                popup.y() - self.height() - popup.height()
            )
            popup.show()

        QTimer.singleShot(0, reposition)
# <<< UPWARDS COMBO BOX <<<