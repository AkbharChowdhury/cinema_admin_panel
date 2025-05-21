from pydantic import BaseModel


from databases.db import  MyDatabase
class SearchMovie(BaseModel):
    title: str
    genre: str
    __db: MyDatabase = MyDatabase()

    @staticmethod
    def any_genres():
        return 'Any'

    def filter_movie(self):
        return self.__db.fetch_movies(self.title, self.genre)
