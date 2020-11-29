import json
import os.path
from typing import Dict, List

from logic.app.configs import config

_DB_POPULAR: List[Dict] = []
_DB_DETALLE: List[Dict] = []

_POPULAR_JSON = f'{config.DIRECTORIO_HARD_THEMOVIEDB_POPULAR}/popular-movies.json'
_DETAIL_JSON = f'{config.DIRECTORIO_HARD_THEMOVIEDB_POPULAR}/detail-movies.json'


def _cargar_db():
    global _DB_POPULAR, _DB_DETALLE

    with open(_POPULAR_JSON, 'rb+') as archivo:
        _DB_POPULAR = json.load(archivo)

    with open(_DETAIL_JSON, 'rb+') as archivo:
        _DB_DETALLE = json.load(archivo)


def peliculas_populares() -> Dict:
    return _DB_POPULAR


def peliculas_detalle(id) -> Dict:
    return next(filter(lambda m: m['id'] == int(id), _DB_DETALLE), None)


_cargar_db()
