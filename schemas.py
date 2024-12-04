from pydantic import BaseModel

class FilmAdd(BaseModel):
    name: str
    description: str | None = None
    year: int | None
    rating: float

class Film(FilmAdd):
    id : int