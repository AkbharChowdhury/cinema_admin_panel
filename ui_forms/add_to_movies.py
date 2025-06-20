from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit,
                             QMessageBox
                             )

import main_menu as admin_panel
from forms.run_app import RunApp
from models.buttons import MyButton
from models.enter_key import EnterAction
from models.form_validation import AddMovieFormValidation
from models.genres import Genre
from models.messageboxes import MyMessageBox
from models.window import Window
from db import Database


class AddMovieForm(QMainWindow):

    def window_action(self):
        if Window.has_closed_admin_panel():
            self.my_window.show_new_window(admin_panel.AdminPanelWindow())

    def __init__(self):
        super().__init__()
        self.db = Database()
        self.my_window = Window()
        self.setWindowTitle("add movie".title())
        central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Movie"))
        self.txt_movie = QLineEdit(self)
        self.layout.addWidget(self.txt_movie)
        self.genre_checkboxes = Genre.create_genre_checkboxes(self.db)

        [self.layout.addWidget(genre_checkbox) for genre_checkbox in self.genre_checkboxes]
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        btn_add_movie = QPushButton('add movie'.title(), self)
        MyButton.hand_cursor([btn_add_movie])
        btn_add_movie.clicked.connect(self.movie_button_action)
        self.layout.addWidget(btn_add_movie)

    def movie_button_action(self):
        db = self.db
        form = AddMovieFormValidation(self.genre_checkboxes, self.txt_movie)
        if not form.is_valid(): return
        genres: set[int] = Genre.selected_genres(db, self.genre_checkboxes)
        movie_title: str = self.txt_movie.text().strip()
        db.add_movie_and_genres(movie_title, genres)
        form.clear_form()
        MyMessageBox.show_message_box('movie added'.title(), QMessageBox.Icon.Information)
        self.window_action()

    def keyPressEvent(self, evt: QKeyEvent):
        EnterAction.enter(evt, self.movie_button_action)


def main():
    RunApp.run(AddMovieForm)


if __name__ == '__main__':
    main()
