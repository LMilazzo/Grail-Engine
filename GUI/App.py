import sys

from PyQt6.QtWidgets import QApplication

from GUI.MainWindow import MainWindow

def main():

    # App System ARGS
    app = QApplication(sys.argv)

    # Main Window
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    