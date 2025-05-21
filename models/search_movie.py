from pydantic import BaseModel


from db import  Database
class SearchMovie(BaseModel):
    title: str
    genre: str
    __db: Database = Database()

    @staticmethod
    def any_genres():
        return 'Any'

    def filter_movie(self):
        return self.__db.fetch_movies(self.title, self.genre)
