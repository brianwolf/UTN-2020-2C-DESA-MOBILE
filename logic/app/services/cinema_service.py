import math
import os
from datetime import time
from typing import List
from uuid import UUID, uuid4

from logic.app.models.cinema import Cinema, Location
from logic.app.repositories import cinema_repository


def guardar_cinema(cinema: Cinema) -> UUID:
    return cinema_repository.guardar_cinema(cinema)


def todos_los_cinema() -> List[Cinema]:
    return cinema_repository.todos_los_cinema()


def todos_los_cinema_mas_cercano(location: Location) -> List[Cinema]:

    def ordenamiento(c: Cinema):
        x = location.longitude - c.location.longitude
        y = location.latitude - c.location.latitude
        return math.sqrt((x**2 + y**2))

    return sorted(cinema_repository.todos_los_cinema(), key=ordenamiento)


def borrar_cinema(id: UUID) -> Cinema:
    return cinema_repository.borrar_cinema(id)


def buscar_cinema(id: UUID) -> Cinema:
    return cinema_repository.buscar_cinema(id)


def ocupar_places(id_cinema: UUID, movie_time: time, places_name: List[str]):
    cinema = buscar_cinema(id_cinema)
    time_table = cinema.buscar_time_table(movie_time)

    for pn in places_name:
        time_table.ocupar_place(pn)

    borrar_cinema(id_cinema)
    guardar_cinema(cinema)
