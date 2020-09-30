from flask import Blueprint, jsonify, render_template, request
from logic.app.configs import config
from logic.libs.logger.logger import log
from pip._vendor.requests import get

blue_print = Blueprint('pagina_peliculas', __name__,
                       url_prefix='/proxy/v1/themoviedb')


@blue_print.route('/<path:path>')
def proxy(path):

    host = config.PAG_PELICULAS_URL
    sufijo_api_key = f'?api_key={config.PAG_PELICULAS_API_KEY}'

    url_final = f'{host}{path}{sufijo_api_key}'
    log().info(f'URL a redireccionar -> {url_final}')

    return get(url_final).content
