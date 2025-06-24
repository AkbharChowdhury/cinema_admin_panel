from PyQt6.QtWidgets import QApplication, QWidget
import operator


class Window:
    def __init__(self):
        self.__w = None

    @staticmethod
    def admin_window_title() -> str:
        return 'admin panel'.title()

    def show_new_window(self, win: QWidget) -> None:
        self.__w = win
        self.__w.show()

    @staticmethod
    def has_closed_existing_admin_panel() -> bool:
        for win in QApplication.topLevelWidgets():
            if operator.eq(win.windowTitle(), Window.admin_window_title()):
                win.close()
                return True
        return False

    @staticmethod
    def close_form(window_title: str) -> None:
        for win in QApplication.topLevelWidgets():
            if operator.eq(win.windowTitle(), window_title):
                win.destroy(True)
