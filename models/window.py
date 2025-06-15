from PyQt6.QtWidgets import QApplication
import operator


class Window:
    @staticmethod
    def admin_window_title():
        return 'admin panel'.title()

    def show_new_window(self, win):
        self.w = win
        self.w.show()

    @staticmethod
    def has_closed_admin_panel():

        for win in QApplication.topLevelWidgets():
            if operator.eq(win.windowTitle(), Window.admin_window_title()):
                win.close()
                return True
        return False
