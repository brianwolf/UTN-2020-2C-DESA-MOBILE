from flask import Blueprint, jsonify, render_template

from logic.app.configs import config

blue_print = Blueprint('pagina_peliculas', __name__,
                       url_prefix='/proxy/v1/themoviedb')


@blue_print.route('/<path:path>')
def proxy(path):
    return {'ruta': path}
