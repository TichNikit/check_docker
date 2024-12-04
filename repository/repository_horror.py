from typing import Optional

from sqlalchemy import select

from database import new_session, Film_horror
from schemas import FilmAdd, Film


class FilmRepository:
    @classmethod
    async def add_one(cls, data: FilmAdd):
        async with new_session() as session:
            film_dict = data.model_dump() #создаем словарь из модели
            film = Film_horror(**film_dict)
            session.add(film)
            await session.flush()
            await session.commit()
            return film.id

    @classmethod
    async def find_all(cls) -> list[Film]:
        async with new_session() as session:
            query = select(Film_horror)
            result = await session.execute(query)
            film_models = result.scalars().all()
            return film_models

    @classmethod
    async def find_one(cls, film_id: int):
        async with new_session() as session:
            query = select(Film_horror).where(Film_horror.id == film_id)
            result = await session.execute(query)
            film = result.scalar()
            return film

    @classmethod
    async def update_one(cls, data: FilmAdd, film_id: int):
        async with new_session() as session:
            film = await session.get(Film_horror, film_id)
            if film is None:
                return None
            film.name = data.name
            film.description = data.description
            film.year = data.year
            film.rating = data.rating
            await session.commit()
            return film.id


    @classmethod
    async def delete_one(cls, film_id: int) -> Optional[int]:
        async with new_session() as session:
            film = await session.get(Film_horror, film_id)
            if film is None:
                return None
            await session.delete(film)
            await session.commit()
            return film_id
