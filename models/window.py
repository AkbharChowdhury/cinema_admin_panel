from PyQt6.QtWidgets import QApplication


class Window:
    def show_new_window(self, win):
        self.w = win
        self.w.show()

    @staticmethod
    def has_closed_admin_panel():
        for win in QApplication.topLevelWidgets():
            if win.windowTitle() == 'Admin Panel'.title():
                win.close()
                return True
        return False
