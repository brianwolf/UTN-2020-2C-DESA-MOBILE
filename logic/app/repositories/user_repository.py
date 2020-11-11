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


def _actualizar_logins():

    global _LOGIN

    nuevo_diccionario = {}
    hoy = datetime.now()

    for k, v in _LOGIN.items():

        if hoy.month == v.last_conection.month and (hoy.day - v.last_conection.day) >= 1:
            continue

        nuevo_diccionario[k] = v

    _LOGIN = nuevo_diccionario


def login_user(login: Login) -> UUID:

    _actualizar_logins()

    for user in _DB:
        if user.login == login:

            token = uuid4()
            user.last_conection = datetime.now()

            _LOGIN[token] = user

            return token

    return None


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


_cargar_db()
