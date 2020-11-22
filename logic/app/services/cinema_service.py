import math
import os
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


def borrar_cinema(id: uuid4) -> Cinema:
    return cinema_repository.borrar_cinema(id)


def buscar_cinema(id: uuid4) -> Cinema:
    return cinema_repository.buscar_cinema(id)


def ocupar_places(id_cinema: uuid4, places_name: List[str]):
    #TODO: hacer
    pass
