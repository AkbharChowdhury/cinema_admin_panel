from enum import Enum, auto

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel


class MovieColumn(Enum):
    TITLE = 0
    GENRES = auto()

class MovieTable:

    def create_model(self, parent):
        model = QStandardItemModel(0, len(MovieColumn), parent)
        horizontal = Qt.Orientation.Horizontal
        for column in MovieColumn:
            model.setHeaderData(column.value, horizontal, column.name.title())
        return model

    @staticmethod
    def add_movies(model: QStandardItemModel, movies: list[dict[str, str]]):
        movies.reverse()
        for movie in movies:
            model.insertRow(0)
            for key, value in movie.items():
                if key == 'MOVIE_ID': continue
                model.setData(model.index(0, MovieColumn[key].value), value)
