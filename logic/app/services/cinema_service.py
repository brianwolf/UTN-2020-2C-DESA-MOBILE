import math
import os
from datetime import date, time
from typing import List
from uuid import UUID, uuid4

from logic.app.models.cinema import Cinema, Location, TimeTablesFilters
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


def ocupar_seats(cinema_id: UUID, filters: TimeTablesFilters,  seats_ids: List[int]):

    cinema = buscar_cinema(cinema_id)
    time_table = cinema.timetables_por_filters(filters)

    if len(time_table) != 1:
        # TODO mejorar excepcion
        raise Exception(
            'Error en buscar horarios que coincidan con lo pedido dentro del cine')

    time_table = time_table[0]

    if list(filter(lambda s: s.id in seats_ids and not s.enable, time_table.seats)):
        # TODO mejorar excepcion
        raise Exception(
            'hay butacas seleccionadas que estan ocupadas')

    for s_id in seats_ids:
        time_table.ocupar_seat(s_id)

    borrar_cinema(cinema_id)
    guardar_cinema(cinema)
