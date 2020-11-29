import json
import os.path
from datetime import date, time, timedelta
from typing import List
from uuid import UUID, uuid4

from logic.app.configs import config
from logic.app.models.cinema import Cinema, Location, Seat, Timetable
from logic.app.repositories import movie_repository

_DIRECOTRIO_JSON: str = f'{config.DIRECTORIO_DB}/cinema.json'
_DB: List[Cinema] = []


def _cinemas_hard() -> List[Cinema]:

    movies_ids = [
        d.get('id')
        for d in movie_repository.peliculas_populares()
    ]

    seats = [
        Seat(id=i, enable=True)
        for i in range(1, 11)
    ]

    t_1 = time(hour=12)
    t_2 = time(hour=17)
    t_3 = time(hour=20)
    t_4 = time(hour=23)

    timetables = []

    i = 0
    dia = date(year=2020, month=12, day=1)
    while i < len(movies_ids):

        id_1 = movies_ids[i]
        id_2 = movies_ids[i+1] if i+1 < len(movies_ids) else None

        timetables.extend([
            Timetable(movie_id=id_1, movie_date=dia,
                      movie_time=t_1, seats=seats, price=600, room=1),
            Timetable(movie_id=id_1, movie_date=dia,
                      movie_time=t_3, seats=seats, price=600, room=1),

            Timetable(movie_id=id_1, movie_date=dia + timedelta(days=7),
                      movie_time=t_1, seats=seats, price=600, room=1),
            Timetable(movie_id=id_1, movie_date=dia + timedelta(days=7),
                      movie_time=t_3, seats=seats, price=600, room=1),
        ])

        if id_2:
            timetables.extend([
                Timetable(movie_id=id_2, movie_date=dia,
                          movie_time=t_2, seats=seats, price=600, room=1),
                Timetable(movie_id=id_2, movie_date=dia,
                          movie_time=t_4, seats=seats, price=600, room=1),

                Timetable(movie_id=id_2, movie_date=dia + timedelta(days=7),
                          movie_time=t_2, seats=seats, price=600, room=1),
                Timetable(movie_id=id_2, movie_date=dia + timedelta(days=7),
                          movie_time=t_4, seats=seats, price=600, room=1)
            ])

        i += 2
        dia += timedelta(days=1)

    return [
        Cinema(
            name='Multiplex Monumental Lavalle',
            description='Cines Multiplex lleva adelante la operación de este complejo que es el único que permanece en la peatonal Lavalle donde supieron funcionar, en las épocas de gloria, más de 28 salas de cine.',
            adress='Lavalle 780, C1047 AAP, Buenos Aires',
            stars=4.1,
            location=Location(latitude=-34.60245,
                              longitude=-58.377785),
            image_path=f'{config.DIRECTORIO_IMG_CINEMA}/monumental.jpg',
            timetables=timetables,
            id=UUID("7f55a7f0-10a8-48f2-a4fa-49cc48d0589c"),
            price=600
        ),
        Cinema(
            name='Gaumont',
            description='El Cine Gaumont es una sala cinematográfica que se encuentra frente a la Plaza Congreso, en la ciudad de Buenos Aires. Desde el año 2003 funciona en él el Espacio INCAA Km. 0. El cine fue fundado en 1912 con el nombre de Cinematógrafo de la Plaza del Congreso, pero a los pocos años ya se llamaba Gaumont Theatre, en referencia a Leon Gaumont.',
            adress='Av. Rivadavia 1635, C1033 CABA',
            stars=4.6,
            location=Location(latitude=-34.6089591,
                              longitude=-58.3896579),
            image_path=f'{config.DIRECTORIO_IMG_CINEMA}/gaumont.jpg',
            timetables=timetables,
            id=UUID("0c5d04cd-5582-4113-bfe1-e17fc39dbceb"),
            price=500
        ),
        Cinema(
            name='Hoyts Abasto',
            description='Cinemark Hoyts es una cadena de cines de argentina. Cuenta con complejos ubicados en todo el país',
            adress='Av. Corrientes 3247, C1193AAE CABA',
            stars=4.3,
            location=Location(latitude=-34.6032898,
                              longitude=-58.4108409),
            image_path=f'{config.DIRECTORIO_IMG_CINEMA}/hoyts.jpg',
            timetables=timetables,
            id=UUID("6ac18d0f-5581-4024-a0ca-e26ca435e66a"),
            price=550
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
