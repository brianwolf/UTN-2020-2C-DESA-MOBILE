from flask import Blueprint, jsonify, render_template
from logic.app.services import movie_service

blue_print = Blueprint('movies', __name__, url_prefix='/api/v1/movies')


@blue_print.route('/popular', methods=['GET'])
def peliculas_populares():

    return jsonify(results=movie_service.peliculas_populares()), 200


@blue_print.route('/<id>', methods=['GET'])
def peliculas_detalle(id: int):

    resultado = movie_service.peliculas_detalle(id)
    if not resultado:
        return '', 204

    return jsonify(resultado), 200
