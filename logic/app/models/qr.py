from dataclasses import dataclass
from uuid import uuid4


@dataclass
class Qr(object):
    id: uuid4 = uuid4()
    imagen_contenido: bytes
    imagen_ruta: str
