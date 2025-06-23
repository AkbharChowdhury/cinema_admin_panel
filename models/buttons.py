from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QPushButton


class MyButton:
    @staticmethod
    def hand_cursor(buttons: list[QPushButton]) -> None:
        for button in buttons:
            button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
