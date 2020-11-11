import json
import os.path
from typing import List
from uuid import uuid4

from logic.app.configs import config
from logic.app.models.qr import Qr

_DIRECOTRIO_JSON: str = f'{config.DIRECTORIO_DB}/qr.json'
_DB: List[Qr] = []


def _cargar_db():
    """
    guarda la db en un json
    """
    global _DB

    if not os.path.exists(_DIRECOTRIO_JSON):
        with open(_DIRECOTRIO_JSON, 'w+') as db:
            db.write('[]')

    with open(_DIRECOTRIO_JSON, 'rb+') as db:
        _DB = [Qr.from_json(d) for d in json.load(db)]


def _actualizar_db():
    """
    guarda la db en un json
    """
    with open(_DIRECOTRIO_JSON, 'w+') as db:
        json.dump([o.to_json() for o in _DB], db)


def guardar_qr(qr: Qr):
    """
    guarda un qr en la db
    """
    if qr in _DB:
        _DB.remove(qr)

    _DB.append(qr)
    _actualizar_db()


def buscar_qr(id: uuid4) -> Qr:
    """
    busca un qr en la base de datos
    """
    _cargar_db()
    for qr in _DB:
        if qr.id == id:
            return qr

    return None
