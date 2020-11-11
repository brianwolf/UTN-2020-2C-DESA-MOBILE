from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import uuid4


@dataclass
class Login(object):
    user: str
    password: str


@dataclass
class Tarjetas(object):
    numero: str
    nombre_titular: str
    vencimiento: str


@dataclass
class Usuario(object):
    id: uuid4 = uuid4()
    nombre: str
    fecha_ultima_conexion: datetime
    tarjetas: List[Tarjetas]
