import os
from typing import List
from uuid import uuid4

import qrcode
from logic.app.configs import config
from logic.app.models.qr import Qr
from logic.app.repositories import qr_repository


def crear_qr() -> Qr:
    """
    crea un qr
    """
    qr = Qr()

    imagen = qrcode.make(str(qr.id))
    imagen.save(qr.imagen_ruta)

    qr_repository.guardar_qr(qr)

    return qr


def buscar_qr(id: uuid4) -> Qr:
    """
    busca un qr
    """
    return qr_repository.buscar_qr(id)


def todos_los_qr() -> List[Qr]:
    """
    busca todos los qrs
    """
    return qr_repository.todos_los_qr()


def borrar_qr(id: uuid4) -> Qr:
    """
    borra el qr si existe
    """
    qr = qr_repository.borrar_qr(id)
    if qr is not None:
        os.remove(qr.imagen_ruta)

    return qr
