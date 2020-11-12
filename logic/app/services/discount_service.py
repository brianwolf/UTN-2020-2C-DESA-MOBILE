import os
from typing import List
from uuid import UUID

from logic.app.models.discount import Discount
from logic.app.models.user import User
from logic.app.repositories import discount_repository


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
