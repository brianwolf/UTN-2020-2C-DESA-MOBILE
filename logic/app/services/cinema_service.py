import math
import os
from datetime import time
from typing import List
from uuid import UUID, uuid4

from logic.app.models.cinema import Cinema, TimeTablesFilters, Location
from logic.app.repositories import cinema_repository


def guardar_cinema(cinema: Cinema) -> UUID:
    return cinema_repository.guardar_cinema(cinema)


def todos_los_cinema_por_filtros(filters: TimeTablesFilters = TimeTablesFilters()) -> List[Cinema]:

    cines = cinema_repository.todos_los_cinema()

    if filters.movie_id:

        def cine_tiene_peli(c): return any(filter(
            lambda tt: tt.movie_id == filters.movie_id,
            c.timetables
        ))

        cines = filter(cine_tiene_peli, cines)

    return cines


def todos_los_cinema() -> List[Cinema]:
    return cinema_repository.todos_los_cinema()


def todos_los_cinema_mas_cercano(location: Location, filters: TimeTablesFilters = TimeTablesFilters()) -> List[Cinema]:

    def ordenamiento(c: Cinema):
        x = location.longitude - c.location.longitude
        y = location.latitude - c.location.latitude
        return math.sqrt((x**2 + y**2))

    return sorted(todos_los_cinema_por_filtros(filters=filters), key=ordenamiento)


def borrar_cinema(id: UUID) -> Cinema:
    return cinema_repository.borrar_cinema(id)


def buscar_cinema(id: UUID) -> Cinema:
    return cinema_repository.buscar_cinema(id)


def ocupar_seats(id_cinema: UUID, movie_time: time, seats_name: List[int]):
    cinema = buscar_cinema(id_cinema)
    time_table = cinema.buscar_time_table(movie_time)

    for pn in seats_name:
        time_table.ocupar_place(pn)

    borrar_cinema(id_cinema)
    guardar_cinema(cinema)
