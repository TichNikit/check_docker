from typing import Annotated

from fastapi import APIRouter, Depends

from repository.repository_history import FilmRepository
from schemas import FilmAdd, Film

# from repository import TaskRepository


router_history = APIRouter(prefix='/film_hist', tags=["Исторические фильмы"])


@router_history.post('')
async def add_film(film: Annotated[FilmAdd, Depends()]):
    task_id = await FilmRepository.add_one(film)
    return {'request': 'ok', 'task_id': task_id}


@router_history.put('')
async def update_film(film: Annotated[FilmAdd, Depends()], film_id: int):
    task_id = await FilmRepository.update_one(film, film_id)
    return {'request': 'ok', 'task_id': task_id}


@router_history.delete('')
async def delet_film(film_id: int):
    task_id = await FilmRepository.delete_one(film_id)
    return {'request': 'ok', 'task_id': task_id}


@router_history.get('')
async def get_film() -> list[Film]:
    films = await FilmRepository.find_all()
    return films


@router_history.get('/one')
async def get_film_one(film_id: int):
    films = await FilmRepository.find_one(film_id)
    return films
