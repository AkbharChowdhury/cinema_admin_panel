from pydantic import BaseModel, Field
from typing_extensions import TypedDict, ReadOnly

from models.genres import Genre
import operator


class MovieDict(TypedDict):
    movie_id: ReadOnly[int]
    title: ReadOnly[str]
    genres: list[str]


class Movie(BaseModel):
    movie_id: int
    title: str = Field(min_length=2)
    genres: list[str]


def filter_movie(db, movie_id: int):
    movies = db.fetch_movies()
    movie = list(filter(lambda x: operator.eq(movie_id, x['movie_id']), movies))[0]

    genres: list[str] = movie.get('genres').split(Genre.genre_split())
    movie.update({'genres': genres})
    my_movie: Movie = Movie(**movie)
    print(list(filter(lambda x: operator.eq(movie_id, x['movie_id']), movies)))
    print(my_movie)
    print(my_movie.genres)
    print(my_movie.title)
