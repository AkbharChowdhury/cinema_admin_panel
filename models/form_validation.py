from PyQt6.QtWidgets import QCheckBox, QLineEdit
from pydantic import BaseModel, ConfigDict
from operator import eq
from models.messageboxes import MyMessageBox
class ErrorMessage:
    @staticmethod
    def movie_error_message() -> str:
        return 'Please choose a movie from the table'


class AddMovieFormValidation(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    checkbox_genres: list[QCheckBox]
    txt_movie: QLineEdit

    def clear(self) -> None:
        [checkbox.setChecked(False) for checkbox in self.checkbox_genres if checkbox.isChecked()]
        self.txt_movie.clear()

    def is_valid(self) -> bool:

        if eq(self.txt_movie.text().strip(), ''):
            MyMessageBox.show_message_box('Movie title is required!')
            return False
        if not self.__has_selected_genre():
            MyMessageBox.show_message_box('Please choose a genre!')
            return False
        return True

    def __has_selected_genre(self) -> bool:
        return any(list(filter(lambda checkbox: checkbox.isChecked(), self.checkbox_genres)))


