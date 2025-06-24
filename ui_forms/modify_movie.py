from PyQt6.QtWidgets import (QApplication,
                             QMainWindow,
                             QWidget,
                             QVBoxLayout,
                             QLabel,
                             QPushButton,
                             QLineEdit, QMessageBox, QCheckBox, QGridLayout, QFormLayout
                             )

import main_menu as admin_panel
from db import Database
from forms.run_app import RunApp
from models.buttons import MyButton
from models.form_validation import AddMovieFormValidation
from models.genres import Genre
from models.grid_layout_manager import GridLayoutManager
from models.messageboxes import MyMessageBox
from models.movie_info import MovieInfo
from models.window import Window


class EditMovieForm(QWidget):

    def __init__(self):
        super().__init__()
        # self.setWindowTitle("Edit Movie")
        self.db = Database()
        self.my_window = Window()

        self.txt_movie = QLineEdit(self)

        self.txt_movie.returnPressed.connect(lambda _: self.movie_button_action)

        btn_undo_title = QPushButton('undo'.title(), self)
        btn_undo_genres = QPushButton('undo genres'.title(), self)
        btn_edit_movie = QPushButton('update movie'.title(), self)

        outer_layout = QVBoxLayout()

        top_layout = QGridLayout()

        top_layout.addWidget(QLabel('movie'.title()), 0, 0)
        top_layout.addWidget(self.txt_movie, 1, 0)
        top_layout.addWidget(btn_undo_title, 1, 1)

        undo_genre_layout = QVBoxLayout()
        undo_genre_layout.addWidget(btn_undo_genres)

        genre_options_layout = QVBoxLayout()

        self.genre_checkboxes: list[QCheckBox] = Genre.create_genre_checkboxes(self.db)

        [genre_options_layout.addWidget(genre_checkbox) for genre_checkbox in self.genre_checkboxes]

        bottom_layout = QVBoxLayout()
        bottom_layout.addWidget(btn_edit_movie)

        outer_layout.addLayout(top_layout)
        outer_layout.addLayout(undo_genre_layout)
        outer_layout.addLayout(genre_options_layout)
        outer_layout.addLayout(bottom_layout)

        self.setLayout(outer_layout)

        btn_edit_movie.clicked.connect(self.movie_button_action)
        btn_undo_title.clicked.connect(self.undo_title)
        btn_undo_genres.clicked.connect(self.undo_genres)

        self.movie_data: dict[str, str] = self.fetch_movie_details(MovieInfo.MOVIE_ID)
        self.setWindowTitle(self.movie_data.get('title', 'edit movie'.title()))

        self.txt_movie.setText(self.movie_data['title'])
        self.undo_genres()
        MyButton.hand_cursor([btn_edit_movie, btn_undo_title, btn_undo_genres])

    def undo_title(self) -> None:
        self.txt_movie.setText("")
        self.txt_movie.setText(self.movie_data['title'])

    def undo_genres(self) -> None:
        [checkbox.setChecked(False) for checkbox in self.genre_checkboxes]
        [checkbox.setChecked(True) for checkbox in self.genre_checkboxes if
         checkbox.text() in self.movie_data['genres']]

    def movie_button_action(self):
        db = self.db
        form = AddMovieFormValidation(checkbox_genres=self.genre_checkboxes, txt_movie=self.txt_movie)

        if not form.is_valid(): return
        genres: set[int] = Genre.selected_genres(db, self.genre_checkboxes)

        if (movie_text := self.txt_movie.text().strip()) != self.movie_data.get('title'):
            db.update_movie(MovieInfo.MOVIE_ID, movie_text)
        db.delete('movie_id', 'movie_genres', MovieInfo.MOVIE_ID)
        db.add_movie_genres(MovieInfo.MOVIE_ID, genres)
        MyMessageBox.show_message_box('Movie updated', QMessageBox.Icon.Information)
        self.window_action()

    def window_action(self) -> None:
        if Window.has_closed_existing_admin_panel():
            Window.close_form(window_title=self.movie_data.get('title'))
            self.my_window.show_new_window(admin_panel.AdminPanelWindow())

    def fetch_movie_details(self, movie_id: int) -> dict[str, str]:
        return list(filter(lambda movie: movie['movie_id'] == movie_id, self.db.fetch_movies()))[0]


def main():
    RunApp.run(EditMovieForm, (700, 700))


if __name__ == '__main__':
    db = Database()
    main()
