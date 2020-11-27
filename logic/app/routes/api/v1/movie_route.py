import json

from flask import Blueprint, jsonify, render_template, send_file
from logic.app.configs import config

blue_print = Blueprint('movies', __name__, url_prefix='/api/v1/movies')


_POPULAR_JSON = f'{config.DIRECTORIO_HARD_THEMOVIEDB_POPULAR}/popular-movies.json'
_DETAIL_JSON = f'{config.DIRECTORIO_HARD_THEMOVIEDB_POPULAR}/detail-movies.json'


@blue_print.route('/populars', methods=['GET'])
def peliculas_populares():

    with open(_POPULAR_JSON, 'rb+') as archivo:
        datos = json.load(archivo)

    return jsonify(datos), 200


@blue_print.route('/<id>', methods=['GET'])
def peliculas_detalle(id: int):

    with open(_DETAIL_JSON, 'rb+') as archivo:
        datos = json.load(archivo)

    resultado = next(filter(lambda m: m['id'] == int(id), datos), None)
    if not resultado:
        return '', 204

    return jsonify(resultado), 200
