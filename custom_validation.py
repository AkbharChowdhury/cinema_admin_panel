class Validation:
    @staticmethod
    def is_valid_genre(genres: set[int]) -> bool:
        is_genre_set: bool = isinstance(genres, set)
        contain_ints: bool = all(isinstance(elem, int) for elem in genres)
        return is_genre_set and contain_ints

    @staticmethod
    def is_valid_movie(title: str, genres: set[int]) -> bool:
        errors: list[str] = []
        if not title or title.strip() == '':
            errors.append('title is required!'.capitalize())
        if not Validation.is_valid_genre(genres):
            errors.append('genre must be a set and contain integer values only!'.capitalize())

        has_errors: bool = len(errors) > 0

        if has_errors:
            raise ValueError(
                f'Whoops, something went wrong! there is an error with the data submitted. Please review errors and try again!\n{'\n'.join(errors)}')
        return not has_errors
