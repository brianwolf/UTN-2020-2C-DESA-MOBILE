import os
from typing import List
from uuid import UUID

from logic.app.errors.discount_error import DiscountErrors
from logic.app.models.discount import Discount
from logic.app.models.user import DiscountUser, User
from logic.app.repositories import discount_repository
from logic.app.services import user_service
from logic.libs.excepcion.excepcion import AppException


def guardar_discount(discount: Discount) -> UUID:
    return discount_repository.guardar_discount(discount)


def todos_los_discount() -> List[Discount]:
    return discount_repository.todos_los_discount()


def borrar_discount(id: UUID) -> Discount:
    return discount_repository.borrar_discount(id)


def buscar_discount(id: UUID) -> Discount:
    return discount_repository.buscar_discount(id)


def buscar_discount_por_user(user: User) -> List[Discount]:

    user_discounts_ids = [o.id for o in user.discounts]
    discounts = todos_los_discount()

    return [
        d
        for d in discounts
        if d.id in user_discounts_ids
    ]


def agregar_discount_a_user(user: User, discount_user: DiscountUser):

    discount = buscar_discount(discount_user.id)
    if not discount:
        msj = f'El descuento con id {discount_user.id} no fue encontrado'
        raise AppException(DiscountErrors.DESCUENTO_TO_ENCONTRADO, mensaje=msj)

    user.discounts.append(discount_user)
    user_service.guardar_user(user)
