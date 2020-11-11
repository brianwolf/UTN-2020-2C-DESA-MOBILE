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
