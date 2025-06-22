from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QComboBox, \
    QGridLayout, QPushButton, QLabel, QGroupBox, QTreeView, QHBoxLayout, QMessageBox, QAbstractItemView

import add_to_movies as add_movie_form
import modify_movie as edit_movie_form
from db import Database
from models.buttons import MyButton
from models.form_validation import ErrorMessage
from models.grid_layout_manager import GridLayoutManager
from models.messageboxes import MyMessageBox
from models.movie_info import MovieInfo
from models.movie_table import MovieTable, MovieColumn, CustomTreeView
from models.search_movie import SearchMovie
from models.window import Window
from forms.run_app import RunApp

MOVIE_ID_COLUMN: str = 'MOVIE_ID'


class AdminPanelWindow(QWidget):
    def fetch_filtered_movies(self) -> list[dict[str, str]]:
        title = MovieColumn.TITLE.name
        genres = MovieColumn.GENRES.name
        return [{
            MOVIE_ID_COLUMN: movie.get(MOVIE_ID_COLUMN.lower()),
            title: movie.get(title.lower()),
            genres: movie.get(genres.lower()),
        } for movie in self.search.filter_movie()]

    def edit_movie(self):
        if self.is_selection_empty():
            self.__show_error_message()
            return

        self.update_movie_list()
        MovieInfo.MOVIE_ID = self.movies[self.get_selected_table_index()].get('MOVIE_ID')
        self.my_window.show_new_window(edit_movie_form.EditMovieForm())

    def update_movie_list(self) -> None:
        self.movies = self.fetch_filtered_movies()

    def text_changed(self, text):
        self.search.title = text
        self.populate_table()

    def combobox_changed(self):
        genre_text = '' if self.combobox_genres.currentText() == SearchMovie.any_genres() else self.combobox_genres.currentText()
        self.search.genre = genre_text
        self.populate_table()

    def __show_error_message(self) -> None:
        MyMessageBox.show_message_box(ErrorMessage.movie_error_message(), QMessageBox.Icon.Critical)

    def is_selection_empty(self):
        return not self.tree.selectedIndexes()

    def delete_movie(self):
        if self.is_selection_empty():
            self.__show_error_message()
            return

        if MyMessageBox.has_confirmed(self, 'Are you sure you want to delete this movie?'):
            self.update_movie_list()
            self.__delete_selected_movie()

    def __delete_selected_movie(self) -> None:
        selected_movie_index: int = self.get_selected_table_index()
        movie_id_col: str = MOVIE_ID_COLUMN
        movie_id: int = int(self.movies[selected_movie_index].get(movie_id_col))
        self.db.delete(movie_id_col.lower(), 'movies', movie_id)
        self.tree.model().removeRow(selected_movie_index)

    def get_selected_table_index(self) -> int:
        return self.tree.selectedIndexes()[0].row()

    def __init__(self):
        super().__init__()
        self.db = Database()
        self.my_window = Window()
        self.movies = self.db.fetch_movies()
        self.setWindowTitle(Window.admin_window_title())

        left, top, width, height = (10, 10, 640, 450)

        self.setGeometry(left, top, width, height)

        self.movie_title: str = ''
        self.genre: str = ''

        self.search = SearchMovie(title='', genre='')
        self.search.filter_movie()

        self.text_box_movies = QLineEdit()

        outer_layout = QVBoxLayout()
        top_layout = QGridLayout()
        middle_layout = QVBoxLayout()
        bottom_layout = QGridLayout()

        self.text_box_movies.installEventFilter(self)
        self.text_box_movies.textEdited.connect(self.text_changed)

        self.combobox_genres = QComboBox()
        self.combobox_genres.addItem(SearchMovie.any_genres())
        list((self.combobox_genres.addItem(row.name) for row in self.db.fetch_movie_genres()))
        self.combobox_genres.activated.connect(self.combobox_changed)

        GridLayoutManager.add_widgets(top_layout,
                                      [QLabel("Movie"), self.text_box_movies, QLabel("Genre"), self.combobox_genres])

        self.data_group_box = QGroupBox()
        self.tree = CustomTreeView()
        self.tree.setRootIsDecorated(False)
        self.tree.setAlternatingRowColors(True)

        data_layout = QHBoxLayout()
        data_layout.addWidget(self.tree)

        self.data_group_box.setLayout(data_layout)
        self.movie_table = MovieTable()
        self.populate_table()

        btn_add_movie = QPushButton("add movie".title())
        btn_edit_movie = QPushButton("edit movie".title())
        btn_delete_movie = QPushButton("delete movie".title())
        MyButton.hand_cursor([btn_add_movie, btn_edit_movie, btn_delete_movie])

        btn_add_movie.clicked.connect(lambda _: self.my_window.show_new_window(add_movie_form.AddMovieForm()))
        btn_delete_movie.clicked.connect(self.delete_movie)
        btn_edit_movie.clicked.connect(self.edit_movie)

        GridLayoutManager.add_widgets(bottom_layout, [btn_add_movie, btn_edit_movie, btn_delete_movie])

        middle_layout.addWidget(self.data_group_box)

        outer_layout.addLayout(top_layout)
        outer_layout.addLayout(middle_layout)
        outer_layout.addLayout(bottom_layout)
        self.setLayout(outer_layout)
        [self.tree.setColumnWidth(col, 300) for col in range(2)]

    def populate_table(self):
        model = self.movie_table.create_model(self)
        self.tree.setModel(model)
        self.update_movie_list()
        MovieTable.add_movies(model, self.movies)



def main():
    RunApp.run(AdminPanelWindow)


if __name__ == '__main__':
    main()
