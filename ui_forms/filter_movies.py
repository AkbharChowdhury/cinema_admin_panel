from typing_extensions import TypedDict, ReadOnly

from models.genres import Genre
import operator


class Movie(TypedDict):
    movie_id: ReadOnly[int]
    title: ReadOnly[str]
    genres: list[str]


def filter_movie(db, movie_id: int):
    movies = db.fetch_movies()
    data: dict[str, str] = list(filter(lambda x: operator.eq(movie_id, x['movie_id']), movies))[0]
    print(f'{data=}')
    genres: list[str] = data.get('genres').split(Genre.genre_split())
    title: str = data.get('title')
    print(f'{genres=}')
    print(f'{title=}')
    m = Movie(movie_id=movie_id, title=title, genres=genres)
    print(m)
    movie_id, title, genres = m.values()
    print(movie_id)
    print(title)
    print(genres)
