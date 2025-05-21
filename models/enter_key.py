from PyQt6.QtGui import QKeyEvent


class EnterAction:
    @staticmethod
    def enter(evt: QKeyEvent, action):
        enter_key = 16777220
        if evt.key() == enter_key:
            action()