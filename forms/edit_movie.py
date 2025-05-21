from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit,
                             QMessageBox)

from databases.db import Database
from forms import admin_panel
from forms.run_app import RunApp
from models.enter_key import EnterAction
from models.form_validation import AddMovieFormValidation
from models.genres import Genre
from models.messageboxes import MyMessageBox
from models.movie_info import MovieInfo
from models.window import Window


class EditMovieForm(QMainWindow):
    def get_movie_details(self, movie_id: int) -> dict[str, str]:
        return list(filter(lambda x: x['movie_id'] == movie_id, self.db.fetch_movies()))[0]

    def __init__(self):
        super().__init__()
        self.db = Database()
        self.my_window = Window()
        self.setWindowTitle('edit movie'.title())
        central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Movie"))
        self.txt_movie = QLineEdit(self)

        self.layout.addWidget(self.txt_movie)
        self.genre_checkboxes = Genre.create_genre_checkboxes(self.db)
        [self.layout.addWidget(genre_checkbox) for genre_checkbox in self.genre_checkboxes]
        self.movie_data = self.get_movie_details(MovieInfo.MOVIE_ID)
        self.txt_movie.setText(self.movie_data['title'])
        [checkbox.setChecked(True) for checkbox in self.genre_checkboxes if
         checkbox.text() in self.movie_data['genres']]
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        btn_edit_movie = QPushButton('update movie'.title(), self)
        btn_edit_movie.clicked.connect(self.movie_button_action)

        self.layout.addWidget(btn_edit_movie)

    def window_action(self):
        if Window.has_closed_admin_panel():
            self.my_window.show_new_window(admin_panel.AdminPanelWindow())

        for win in QApplication.topLevelWidgets():
            if win.windowTitle() == 'edit movie'.title():
                win.destroy(True)

    def movie_button_action(self):

        db = self.db
        form = AddMovieFormValidation(self.genre_checkboxes, self.txt_movie)
        if not form.is_valid(): return
        selected_genres = [checkbox.text() for checkbox in self.genre_checkboxes if checkbox.isChecked()]
        genre_id_list = set(genre.genre_id for genre in Genre.get_genres(self.db) if genre.name in selected_genres)
        movie_text = self.txt_movie.text().strip()
        if movie_text != self.movie_data.get('title'):  db.update_movie(MovieInfo.MOVIE_ID, movie_text)
        db.delete('movie_id', 'movie_genres', MovieInfo.MOVIE_ID)
        db.add_movie_genres(MovieInfo.MOVIE_ID, genre_id_list)
        MyMessageBox.show_message_box('Movie updated', QMessageBox.Icon.Information)
        self.window_action()

    def keyPressEvent(self, evt: QKeyEvent):
        EnterAction.enter(evt, self.movie_button_action)


def main():
    RunApp.run(EditMovieForm)


if __name__ == '__main__':
    main()
