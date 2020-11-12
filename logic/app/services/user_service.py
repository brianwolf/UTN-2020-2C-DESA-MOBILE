import os
from typing import List
from uuid import uuid4, UUID

from logic.app.models.user import Login, User
from logic.app.repositories import user_repository


def login_user(login: Login) -> UUID:
    return user_repository.login_user(login)


def todos_los_user_logueados() -> List[User]:
    return user_repository.todos_los_user_logueados()


def buscar_user_logueado(token: UUID):
    return user_repository.buscar_user_logueado(token)


def guardar_user(user: User) -> UUID:
    return user_repository.guardar_user(user)


def todos_los_user() -> List[User]:
    return user_repository.todos_los_user()


def borrar_user(id: uuid4) -> User:
    return user_repository.borrar_user(id)


def buscar_user(id: uuid4) -> User:
    return user_repository.buscar_user(id)
