from PyQt6.QtWidgets import QCheckBox
from pydantic import BaseModel, field_validator, Field, NonNegativeInt
from uuid import uuid4
from typing import Union


class MovieGenre(BaseModel):
    class Config:
        frozen = True

    movie_id: NonNegativeInt
    genre_id: NonNegativeInt


class Genre(BaseModel):
    class Config:
        frozen = True

    name: str
    genre_id: Union[str, int] = Field(default=str(uuid4()), gt=0)

    @staticmethod
    def genre_split() -> str:
        return ' | '

    @staticmethod
    def create_genre_checkboxes(db) -> list[QCheckBox]:
        genres: list[Genre] = db.fetch_all_genres()
        return [QCheckBox(genre.name) for genre in genres]

    @staticmethod
    def selected_genres(db, genre_checkboxes: list[QCheckBox]) -> set[int]:
        genres: list[Genre] = db.fetch_all_genres()
        selected_genres: list[str] = [checkbox.text() for checkbox in genre_checkboxes if checkbox.isChecked()]
        return set(genre.genre_id for genre in genres if genre.name in selected_genres)

    @field_validator('name')
    @classmethod
    def validate_name(cls, name: str):
        if name.strip() == '':
            raise Exception('Genre cannot be empty')
        return name


