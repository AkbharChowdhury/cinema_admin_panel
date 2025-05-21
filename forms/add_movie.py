import sys

from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit,
                             QMessageBox
                             )

from forms import admin_panel
from forms.run_app import RunApp
from models.enter_key import EnterAction
from models.genres import Genre
from models.form_validation import AddMovieFormValidation
from models.messageboxes import MyMessageBox
from databases.db import Database
from models.window import Window


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
        btn_add_movie.clicked.connect(self.movie_button_action)
        self.layout.addWidget(btn_add_movie)

    def movie_button_action(self):
        db = self.db
        form = AddMovieFormValidation(self.genre_checkboxes, self.txt_movie)
        if not form.is_valid(): return
        selected_genres: list[str] = [checkbox.text() for checkbox in self.genre_checkboxes if checkbox.isChecked()]
        genre_id_list: set = set(genre.genre_id for genre in Genre.get_genres(db) if genre.name in selected_genres)
        movie_title: str = self.txt_movie.text()
        db.add_movie_and_genres(movie_title, genre_id_list)
        form.clear_form()
        MyMessageBox.show_message_box('movie added'.title(), QMessageBox.Icon.Information)
        self.window_action()

    def keyPressEvent(self, evt: QKeyEvent):
        EnterAction.enter(evt, self.movie_button_action)





def main():
    RunApp.run(AddMovieForm)

if __name__ == '__main__':
    main()
