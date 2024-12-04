# uvicorn main:app --reload
# alembic revision --autogenerate -m "Initial migratio"
from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, status, Body, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from database import create_table
from repository import repository_history, repository_horror, repository_thriller

from routers.router_history import router_history
from routers.router_horror import router_horror
from routers.router_thriller import router_thriller

from bs4 import BeautifulSoup
import requests
import random

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_table()
    print("База готова")
    yield




app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory='templates')
app.mount("/photo", StaticFiles(directory="photo"), name="photo")

app.include_router(router_history)
app.include_router(router_horror)
app.include_router(router_thriller)


@app.get("/")
async def get_welcome(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('welcome.html', {"request": request})


@app.get("/history")
async def get_history_film(request: Request) -> HTMLResponse:
    films = await repository_history.FilmRepository.find_all()
    return templates.TemplateResponse('history_films.html', {"request": request, "films": films})

@app.get("/horror")
async def get_horror_film(request: Request) -> HTMLResponse:
    films = await repository_horror.FilmRepository.find_all()
    return templates.TemplateResponse('horror_films.html', {"request": request, "films": films})

@app.get("/thriller")
async def get_horror_film(request: Request) -> HTMLResponse:
    films = await repository_thriller.FilmRepository.find_all()
    return templates.TemplateResponse('thriller_films.html', {"request": request, "films": films})


@app.get("/movie_for_evening")
async def movie_for_the_evening(request: Request) -> HTMLResponse:
    try:
        url = "https://rutube.ru/feeds/movies/"
        response = requests.get(url)
        data = BeautifulSoup(response.text, "html.parser")

        film_data_list = data.find_all('a', class_='wdp-link-module__link wdp-card-poster-module__posterWrapper')

        film_info_list = []

        for film_data in film_data_list:
            film_url = 'https://rutube.ru' + film_data['href']

            # Получаем изображение
            title_data = film_data.find('div', class_='wdp-card-poster-module__imageWrapper')
            if title_data:
                img_tag = title_data.find('img')
                img_url = img_tag['src'] if img_tag else None
            else:
                img_url = None

            film_title = film_data.find('img')['alt'] if film_data.find('img') else None

            film_info_list.append({
                'title': film_title,
                'url': film_url,
                'image_url': img_url
            })

        total = random.randint(0, len(film_info_list) - 1)
        selected_film = film_info_list[total]
        film_title = selected_film['title']
        film_url = selected_film['url']
        film_image_url = selected_film['image_url']
        error = ""
    except Exception as e:
        error = "Попробуйте ещё раз"
        film_title = ''
        film_url = ''
        film_image_url = ''

    return templates.TemplateResponse('film.html', {
        "request": request,
        "film": film_title,
        "film_url": film_url,
        "film_image_url": film_image_url,
        "error": error
    })


