import os
from typing import List
from uuid import UUID, uuid4

from logic.app.models.user import DiscountUser, Login, User
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


def borrar_user(id: UUID) -> User:
    return user_repository.borrar_user(id)


def buscar_user(id: UUID) -> User:
    return user_repository.buscar_user(id)


def borrar_descuento(id: UUID, id_discount: UUID):

    user = buscar_user(id)
    user.discounts.remove(DiscountUser(id=id_discount))

    borrar_user(id)
    guardar_user(user)
