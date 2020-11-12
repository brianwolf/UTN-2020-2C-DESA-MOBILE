import json
import os.path
from datetime import datetime
from typing import Dict, List
from uuid import UUID, uuid4

from logic.app.configs import config
from logic.app.models.user import Login, User

_DIRECOTRIO_JSON: str = f'{config.DIRECTORIO_DB}/user.json'
_DB: List[User] = []

_LOGIN: Dict[UUID, User] = {}


def _cargar_db():
    global _DB

    if not os.path.exists(_DIRECOTRIO_JSON):
        with open(_DIRECOTRIO_JSON, 'w+') as db:
            db.write('[]')

    with open(_DIRECOTRIO_JSON, 'rb+') as db:
        _DB = [User.from_json(d) for d in json.load(db)]


def _actualizar_db():
    with open(_DIRECOTRIO_JSON, 'w+') as db:
        json.dump([o.to_json() for o in _DB], db)


def _borrar_logueos_viejos():

    global _LOGIN

    hoy = datetime.now()

    _LOGIN = [
        {k: v}
        for k, v in _LOGIN.items()
        if hoy.month == v.last_conection.month and (hoy.day - v.last_conection.day) == 0
    ]


def login_user(login: Login) -> UUID:

    global _LOGIN

    _borrar_logueos_viejos()

    token = next([k for k, v in _LOGIN.items() if v.login == login])
    if token:
        _LOGIN.get(token).last_conection = datetime.now()
        return token

    user = next([u for u in _DB if u.login == login])
    if not user:
        return None

    token = uuid4()
    user.last_conection = datetime.now()
    _actualizar_db()
    _LOGIN[token] = user

    return token


def guardar_user(user: User) -> UUID:
    if user in _DB:
        _DB.remove(user)

    _DB.append(user)
    _actualizar_db()

    return user.id


def buscar_user(id: uuid4) -> User:
    for user in _DB:
        if user.id == id:
            return user

    return None


def todos_los_user() -> List[User]:
    return _DB


def borrar_user(id: uuid4) -> User:
    user = buscar_user(id)
    if user is None:
        return

    _DB.remove(user)
    _actualizar_db()

    return user


def buscar_user_logueado(token: UUID) -> User:
    user = _LOGIN.get(token)
    if not user:
        return None

    login_user(user.login)
    return user


_cargar_db()
