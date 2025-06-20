from PyQt6.QtWidgets import (QApplication,
                             QMainWindow,
                             QWidget,
                             QVBoxLayout,
                             QLabel,
                             QPushButton,
                             QLineEdit, QMessageBox, QCheckBox
                             )

import main_menu as admin_panel
from db import Database
from forms.run_app import RunApp
from models.buttons import MyButton
from models.form_validation import AddMovieFormValidation
from models.genres import Genre
from models.messageboxes import MyMessageBox
from models.movie_info import MovieInfo
from models.window import Window


class EditMovieForm(QMainWindow):
    def fetch_movie_details(self, movie_id: int) -> dict[str, str]:
        return list(filter(lambda movie: movie['movie_id'] == movie_id, self.db.fetch_movies()))[0]

    def __init__(self):
        super().__init__()
        MovieInfo.MOVIE_ID=46
        self.db = Database()
        self.my_window = Window()
        self.setWindowTitle('edit movie'.title())
        central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Movie"))
        self.txt_movie = QLineEdit(self)



        self.layout.addWidget(self.txt_movie)
        btn_undo_title = QPushButton('undo title'.title(), self)
        btn_undo_genres = QPushButton('undo genres'.title(), self)
        self.layout.addWidget(btn_undo_title)
        self.layout.addWidget(btn_undo_genres)

        self.genre_checkboxes: list[QCheckBox] = Genre.create_genre_checkboxes(self.db)
        [self.layout.addWidget(genre_checkbox) for genre_checkbox in self.genre_checkboxes]
        self.movie_data = self.fetch_movie_details(MovieInfo.MOVIE_ID)
        self.txt_movie.setText(self.movie_data['title'])
        [checkbox.setChecked(True) for checkbox in self.genre_checkboxes if
         checkbox.text() in self.movie_data['genres']]
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        btn_edit_movie = QPushButton('update movie'.title(), self)


        btn_edit_movie.clicked.connect(self.movie_button_action)
        btn_undo_title.clicked.connect(self.undo_title)
        btn_undo_genres.clicked.connect(self.undo_genres)

        MyButton.hand_cursor([btn_edit_movie, btn_undo_title, btn_undo_genres])
        self.layout.addWidget(btn_edit_movie)

    def window_action(self):
        if Window.has_closed_admin_panel():
            self.my_window.show_new_window(admin_panel.AdminPanelWindow())

        for win in QApplication.topLevelWidgets():
            if win.windowTitle() == 'edit movie'.title():
                win.destroy(True)
    def undo_title(self):
        print('s')
        self.txt_movie.setText("")
        self.txt_movie.setText(self.movie_data['title'])
    def undo_genres(self):
        for checkbox in self.genre_checkboxes:
            checkbox.setChecked(False)
        [checkbox.setChecked(True) for checkbox in self.genre_checkboxes if
         checkbox.text() in self.movie_data['genres']]
    def movie_button_action(self):

        db = self.db
        form = AddMovieFormValidation(self.genre_checkboxes, self.txt_movie)
        if not form.is_valid(): return
        genres: set[int] = Genre.selected_genres(db, self.genre_checkboxes)

        if (movie_text := self.txt_movie.text().strip()) != self.movie_data.get('title'):
            db.update_movie(MovieInfo.MOVIE_ID, movie_text)
        db.delete('movie_id', 'movie_genres', MovieInfo.MOVIE_ID)
        db.add_movie_genres(MovieInfo.MOVIE_ID, genres)
        MyMessageBox.show_message_box('Movie updated', QMessageBox.Icon.Information)
        self.window_action()


def main():
    RunApp.run(EditMovieForm)


if __name__ == '__main__':
    db = Database()
    main()
