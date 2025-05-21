from typing import Any
from psycopg2 import connect
from psycopg2.extras import DictCursor

from config import load_config
from models.genres import Genre, MovieGenre


class Database:

    def add_movie_and_genres(self, title: str, genre_id_list: set[int]) -> None:
        with connect(**load_config()) as conn, conn.cursor() as cur:
            cur.execute('CALL pr_add_movie_and_genres(%s,%s)', (title, str(genre_id_list)))

    def fetch_movie_genres(self) -> list[Genre]:
        with connect(**load_config()) as conn, conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT genre, genre_id FROM available_movie_genres")
            return list((Genre(name=row['genre'], genre_id=row['genre_id']) for row in cursor.fetchall()))

    def fetch_all_genres(self) -> list[Genre]:
        with connect(**load_config()) as conn, conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT genre AS name, genre_id FROM genres ORDER BY genre")
            return list(Genre(**dict(row)) for row in cursor.fetchall())

    def fetch_movies(self, title: str = '', genre: str = '') -> list[dict[str, Any]]:
        with connect(**load_config()) as conn, conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(f"SELECT movie_id, title, genres FROM fn_get_movies('%{title}%','%{genre}%')")
            movies = (dict(row) for row in cursor.fetchall())
            return sorted(movies, key=lambda m: m.get('title'))

    def add_movie(self, name) -> int:
        with connect(**load_config()) as conn, conn.cursor() as cursor:
            cursor.execute('INSERT INTO movies(title) VALUES(%s) RETURNING movie_id;', ([name]))
            return cursor.fetchone()[0]

    def update_movie(self, movie_id: int, title: str) -> None:
        config = load_config()
        with connect(**config) as conn, conn.cursor() as cur:
            data = dict(movie_id=movie_id, title=title)
            cur.execute(
                f'UPDATE movies SET title = {self.__field('title')} WHERE movie_id = {self.__field('movie_id')}', data)

    def delete(self, id_field: str, table: str, num: int) -> None:
        with connect(**load_config()) as conn, conn.cursor() as cursor:
            cursor.execute(f'DELETE FROM {table} WHERE {id_field} = %s;', ([num]))

    def add_movie_genres(self, movie_id: int, genre_id_list: set[int]) -> None:
        with connect(**load_config()) as conn, conn.cursor() as cur:
            for genre_id in genre_id_list:
                data: dict[str, int] = MovieGenre(movie_id=movie_id, genre_id=genre_id).model_dump()
                cur.execute(
                    f'INSERT INTO movie_genres (movie_id, genre_id) VALUES ({self.__field('movie_id')}, {self.__field('genre_id')})',
                    data)

    def __field(self, name: str):
        return f'%({name})s'


if __name__ == '__main__':
    db = Database()
    print(db.fetch_all_genres())
