import json
import os.path
from datetime import time
from typing import List
from uuid import UUID, uuid4

from logic.app.configs import config
from logic.app.models.cinema import Cinema, Location, Place, Timetable

_DIRECOTRIO_JSON: str = f'{config.DIRECTORIO_DB}/cinema.json'
_DB: List[Cinema] = []


def _cinemas_hard() -> List[Cinema]:

    places = []
    for i in range(1, 30):
        places.append(Place(name=f'B{i}', enable=True))
    for i in range(1, 10):
        places.append(Place(name=f'A{i}', enable=True))
        places.append(Place(name=f'C{i}', enable=True))

    time_15 = time(hour=15)
    time_18 = time(hour=18)
    time_21 = time(hour=21)

    return [
        Cinema(
            name='Multiplex Monumental Lavalle',
            description='Cines Multiplex lleva adelante la operación de este complejo que es el único que permanece en la peatonal Lavalle donde supieron funcionar, en las épocas de gloria, más de 28 salas de cine.',
            adress='Lavalle 780, C1047 AAP, Buenos Aires',
            stars=4.1,
            location=Location(latitude=-34.6010370224385,
                              longitude=-58.39010170379639),
            image_path=f'{config.DIRECTORIO_IMG_CINEMA}/monumental.jpg',
            timetables=[
                Timetable(movie_time=time_15, places=places, price=500),
                Timetable(movie_time=time_18, places=places, price=550),
                Timetable(movie_time=time_21, places=places, price=520)
            ],
            id=uuid4()
        ),
        Cinema(
            name='Gaumont',
            description='El Cine Gaumont es una sala cinematográfica que se encuentra frente a la Plaza Congreso, en la ciudad de Buenos Aires. Desde el año 2003 funciona en él el Espacio INCAA Km. 0. El cine fue fundado en 1912 con el nombre de Cinematógrafo de la Plaza del Congreso, pero a los pocos años ya se llamaba Gaumont Theatre, en referencia a Leon Gaumont.',
            adress='Av. Rivadavia 1635, C1033 CABA',
            stars=4.6,
            location=Location(latitude=-34.6334636,
                              longitude=-58.4682372),
            image_path=f'{config.DIRECTORIO_IMG_CINEMA}/gaumont.jpg',
            timetables=[
                Timetable(movie_time=time_15, places=places, price=550),
                Timetable(movie_time=time_18, places=places, price=600),
                Timetable(movie_time=time_21, places=places, price=570)
            ],
            id=uuid4()
        ),
        Cinema(
            name='Hoyts Abasto',
            description='Cinemark Hoyts es una cadena de cines de argentina. Cuenta con complejos ubicados en todo el país',
            adress='Av. Corrientes 3247, C1193AAE CABA',
            stars=4.3,
            location=Location(latitude=-34.6010370224385,
                              longitude=-58.39010170379639),
            image_path=f'{config.DIRECTORIO_IMG_CINEMA}/hoyts.jpg',
            timetables=[
                Timetable(movie_time=time_15, places=places, price=560),
                Timetable(movie_time=time_18, places=places, price=620),
                Timetable(movie_time=time_21, places=places, price=530)
            ],
            id=uuid4()
        )
    ]


def _cargar_db():
    global _DB

    if not os.path.exists(_DIRECOTRIO_JSON):
        with open(_DIRECOTRIO_JSON, 'w+') as db:
            db.write(json.dumps([c.to_json() for c in _cinemas_hard()]))

    with open(_DIRECOTRIO_JSON, 'rb+') as db:
        _DB = [Cinema.from_json(d) for d in json.load(db)]


def _actualizar_db():
    with open(_DIRECOTRIO_JSON, 'w+') as db:
        json.dump([o.to_json() for o in _DB], db)


def guardar_cinema(cinema: Cinema) -> UUID:
    if cinema in _DB:
        _DB.remove(cinema)

    _DB.append(cinema)
    _actualizar_db()

    return cinema.id


def buscar_cinema(id: uuid4) -> Cinema:
    for cinema in _DB:
        if cinema.id == id:
            return cinema

    return None


def todos_los_cinema() -> List[Cinema]:
    return _DB


def borrar_cinema(id: uuid4) -> Cinema:
    cinema = buscar_cinema(id)
    if cinema is None:
        return

    _DB.remove(cinema)
    _actualizar_db()

    return cinema


_cargar_db()
