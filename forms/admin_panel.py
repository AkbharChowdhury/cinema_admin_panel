import sys

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QApplication, QComboBox, \
    QGridLayout, QPushButton, QLabel, QGroupBox, QTreeView, QHBoxLayout, QMessageBox

from forms import add_movie as add_movie_form
from forms import edit_movie as edit_movie_form

from models.grid_layout_manager import GridLayoutManager
from models.movie_table import MovieTable, MovieColumn
from models.movie_info import MovieInfo

from models.search import SearchMovie
from models.messageboxes import MyMessageBox
from models.window import Window
from models.form_validation import ErrorMessage
from databases.db import  MyDatabase

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
        if not self.tree.selectedIndexes():
            MyMessageBox.show_message_box(MOVIE_ERROR_MESSAGE, QMessageBox.Icon.Warning)
            return
        selected_movie_index = self.get_selected_table_index()
        self.update_movie_list()
        MovieInfo.MOVIE_ID = self.movies[selected_movie_index].get('MOVIE_ID')
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

    def delete_movie(self):
        if not self.tree.selectedIndexes():
            MyMessageBox.show_message_box(MOVIE_ERROR_MESSAGE, QMessageBox.Icon.Warning)
            return

        if MyMessageBox.confirm(self, 'Are you sure you want to delete this movie?') == QMessageBox.StandardButton.Yes:
            selected_movie_index = self.get_selected_table_index()
            self.update_movie_list()
            movie_id_col: str = MOVIE_ID_COLUMN
            movie_id: int = int(self.movies[selected_movie_index].get(movie_id_col))
            self.db.delete(movie_id_col.lower(), 'movies', movie_id)
            self.tree.model().removeRow(selected_movie_index)

    def get_selected_table_index(self):
        return self.tree.selectedIndexes()[0].row()

    def __init__(self):
        super().__init__()
        self.db = MyDatabase()
        self.my_window = Window()
        self.movies = self.db.fetch_movies()
        self.setWindowTitle("admin panel".title())

        left, top, width, height = (10, 10, 640, 450)

        self.setGeometry(left, top, width, height)
        self.movie_title = self.genre = ''
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
        [self.combobox_genres.addItem(row.name) for row in self.db.fetch_movie_genres()]
        self.combobox_genres.activated.connect(self.combobox_changed)

        GridLayoutManager.add_widgets(top_layout,
                                      [QLabel("Movie"), self.text_box_movies, QLabel("Genre"), self.combobox_genres])

        self.data_group_box = QGroupBox()
        self.tree = QTreeView()
        self.tree.setRootIsDecorated(False)
        self.tree.setAlternatingRowColors(True)

        data_layout = QHBoxLayout()
        data_layout.addWidget(self.tree)

        self.data_group_box.setLayout(data_layout)
        self.movie_table = MovieTable()
        self.model = None
        self.populate_table()

        btn_add_movie = QPushButton("add movie".title())
        btn_edit_movie = QPushButton("edit movie".title())
        btn_delete_movie = QPushButton("delete movie".title())

        btn_add_movie.clicked.connect(lambda x: self.my_window.show_new_window(add_movie_form.AddMovieForm()))
        btn_delete_movie.clicked.connect(self.delete_movie)
        btn_edit_movie.clicked.connect(self.edit_movie)

        GridLayoutManager.add_widgets(bottom_layout, [btn_add_movie, btn_edit_movie, btn_delete_movie])

        middle_layout.addWidget(self.data_group_box)

        outer_layout.addLayout(top_layout)
        outer_layout.addLayout(middle_layout)
        outer_layout.addLayout(bottom_layout)
        self.setLayout(outer_layout)
        self.tree.setColumnWidth(0, 300)
        self.tree.setColumnWidth(1, 300)

    def populate_table(self):
        self.model = self.movie_table.create_model(self)
        self.tree.setModel(self.model)
        self.update_movie_list()
        MovieTable.add_movies(self.model, self.movies)


def main():
    app = QApplication(sys.argv)
    window = AdminPanelWindow()
    window.show()
    sys.exit(app.exec())


# if __name__ == '__main__':
#     MOVIE_ERROR_MESSAGE = ErrorMessage.movie_error_message()
#
#     # db = MyDatabase()
#     # print(db)
#
#     # main()

db = MyDatabase()
print('hello')
