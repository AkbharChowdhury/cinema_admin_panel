from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent


class EnterAction:
    @staticmethod
    def enter(evt: QKeyEvent, action):
        if evt.key() == Qt.Key.Key_Return:
            action()
