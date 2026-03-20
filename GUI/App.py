import sys

from PyQt6.QtWidgets import QApplication

from GUI.MainWindow import MainWindow

import subprocess

def main():

    # App System ARGS
    app = QApplication(sys.argv)

        # QUIT LOGIC
    app.aboutToQuit.connect(
        lambda: subprocess.Popen(["python", "HISTORY/Janitor.py"])
    )

    # Main Window
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    