from enum import Enum, auto

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem


class MovieColumn(Enum):
    TITLE = 0
    GENRES = auto()


class MovieTable:
    def create_model(self, parent) -> QStandardItemModel:
        model = QStandardItemModel(0, len(MovieColumn), parent)
        for column in MovieColumn:
            model.setHeaderData(column.value, Qt.Orientation.Horizontal, column.name.title())
        return model

    @staticmethod
    def add_movies(model: QStandardItemModel, movies: list[dict[str, str]]) -> None:
        movies.reverse()
        for movie in movies:
            model.insertRow(0)
            for key, value in movie.items():
                if key == 'MOVIE_ID':
                    continue
                model.setData(model.index(0, MovieColumn[key].value), value)
