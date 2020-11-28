import json
import os.path
from typing import Dict, List

from logic.app.configs import config

_DB: List[Dict] = []

_POPULAR_JSON = f'{config.DIRECTORIO_HARD_THEMOVIEDB_POPULAR}/popular-movies.json'
_DETAIL_JSON = f'{config.DIRECTORIO_HARD_THEMOVIEDB_POPULAR}/detail-movies.json'


def _cargar_db():
    global _DB

    with open(_POPULAR_JSON, 'rb+') as archivo:
        _DB = json.load(archivo)


def peliculas_populares() -> Dict:
    return _DB


def peliculas_detalle(id) -> Dict:
    return next(filter(lambda m: m['id'] == int(id), _DB), None)


_cargar_db()
