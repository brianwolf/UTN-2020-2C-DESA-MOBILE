from dataclasses import dataclass
from uuid import uuid4, UUID

from logic.app.configs import config


@dataclass
class Qr(object):
    id: uuid4
    imagen_ruta: str

    def __init__(self, id=None, imagen_ruta=''):
        self.id = uuid4() if id is None else id
        self.imagen_ruta = f'{config.DIRECTORIO_QR}/{self.id}'

    def __eq__(self, other):
        return self.id == other.id

    def cargar_contenido(self) -> bytes:
        """
        Abre el archivo y devuelve el contenido
        """
        with open(self.imagen_ruta, 'rb') as archivo:
            return archivo.read()

    def to_json(self) -> dict:
        return {
            'id': str(self.id),
            'imagen_ruta': self.imagen_ruta
        }

    @staticmethod
    def from_json(d: dict) -> 'Qr':
        return Qr(id=UUID(str(d['id'])), imagen_ruta=str(d['imagen_ruta']))
