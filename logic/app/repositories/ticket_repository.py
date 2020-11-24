import json
import os.path
from typing import List
from uuid import UUID

from logic.app.configs import config
from logic.app.models.ticket import Ticket

_DIRECOTRIO_JSON: str = f'{config.DIRECTORIO_DB}/tickets.json'
_DB: List[Ticket] = []


def _cargar_db():
    global _DB

    if not os.path.exists(_DIRECOTRIO_JSON):
        with open(_DIRECOTRIO_JSON, 'w+') as db:
            db.write('[]')

    with open(_DIRECOTRIO_JSON, 'rb+') as db:
        _DB = [Ticket.from_json(d) for d in json.load(db)]


def _actualizar_db():
    with open(_DIRECOTRIO_JSON, 'w+') as db:
        json.dump([o.to_json() for o in _DB], db)


def guardar_ticket(ticket: Ticket) -> UUID:
    if ticket in _DB:
        _DB.remove(ticket)

    _DB.append(ticket)
    _actualizar_db()

    return ticket.id


def buscar_ticket(id: UUID) -> Ticket:
    for ticket in _DB:
        if ticket.id == id:
            return ticket

    return None


def todos_los_ticket() -> List[Ticket]:
    return _DB


def borrar_ticket(id: UUID) -> Ticket:
    ticket = buscar_ticket(id)
    if ticket is None:
        return

    _DB.remove(ticket)
    _actualizar_db()

    return ticket


_cargar_db()
