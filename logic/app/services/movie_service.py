import os
from typing import Dict, List
from uuid import UUID, uuid4

from logic.app.models.user import DiscountUser, Login, User
from logic.app.repositories import movie_repository


def peliculas_populares() -> Dict:
    return movie_repository.peliculas_populares()


def peliculas_detalle(id: int) -> Dict:
    return movie_repository.peliculas_detalle(id)
