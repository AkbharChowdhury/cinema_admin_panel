from PyQt6.QtWidgets import QCheckBox, QMessageBox, QLineEdit

from models.messageboxes import MyMessageBox


class ErrorMessage:
    @staticmethod
    def movie_error_message() -> str:
        return 'Please choose a movie from the table'


class AddMovieFormValidation:

    def clear_form(self):
        [checkbox.setChecked(False) for checkbox in self.__checkbox_genres if checkbox.isChecked()]
        self.txt_movie.clear()

    def __init__(self, checkbox_genres, txt_movie: QLineEdit):
        self.__checkbox_genres: list[QCheckBox] = checkbox_genres
        self.txt_movie: QLineEdit = txt_movie

    def is_valid(self):
        if self.txt_movie.text().strip() == '':
            MyMessageBox.show_message_box('Movie title is required!', QMessageBox.Icon.Critical)
            return False
        if not self._has_selected_genre():
            MyMessageBox.show_message_box('Please choose a genre!', QMessageBox.Icon.Critical)
            return False
        return True

    def _has_selected_genre(self):
        return len(list(filter(lambda checkbox: checkbox.isChecked(), self.__checkbox_genres))) > 0
