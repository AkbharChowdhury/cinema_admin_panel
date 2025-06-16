import sys

from PyQt6.QtWidgets import QApplication, QMainWindow


class RunApp:
    @staticmethod
    def run(w: QMainWindow, dimension: None | tuple = None):
        app = QApplication(sys.argv)
        window = w()
        window.show()
        if dimension is not None:
            (width, height) = dimension
            window.resize(width, height)
        sys.exit(app.exec())
