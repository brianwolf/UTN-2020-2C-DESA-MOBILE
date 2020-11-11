import os
from typing import List
from uuid import uuid4, UUID

from logic.app.models.cinema import Cinema
from logic.app.repositories import cinema_repository


def guardar_cinema(cinema: Cinema) -> UUID:
    return cinema_repository.guardar_cinema(cinema)


def todos_los_cinema() -> List[Cinema]:
    return cinema_repository.todos_los_cinema()


def borrar_cinema(id: uuid4) -> Cinema:
    return cinema_repository.borrar_cinema(id)


def buscar_cinema(id: uuid4) -> Cinema:
    return cinema_repository.buscar_cinema(id)
