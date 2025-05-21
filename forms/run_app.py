import sys

from PyQt6.QtWidgets import QApplication, QMainWindow


class RunApp:
    @staticmethod
    def run(w: QMainWindow):
        app = QApplication(sys.argv)
        window = w()
        window.show()
        sys.exit(app.exec())