import os
import requests

from flask import Blueprint, jsonify, request
from logic.app.configs import config
from logic.libs.logger.logger import log

blue_print = Blueprint('pagina_peliculas', __name__,
                       url_prefix='/proxy/v1/themoviedb')


@blue_print.route('/<path:path>', methods=['GET'])
def proxy(path: str):

    url_final = os.path.join(config.PAG_PELICULAS_URL, path)
    url_final = agregar_query_params(url_final, request.args)

    log().info(f'URL a redireccionar -> {url_final}')

    respuesta = requests.get(url_final)
    try:
        return jsonify(respuesta.json())

    except Exception as e:
        return respuesta.content


def tiene_query_param(url: str) -> bool:
    return '?' in url


def agregar_query_params(url: str, params: dict) -> str:

    query_params = {
        'language': config.PAG_PELICULAS_IDIOMA,
        'api_key': config.PAG_PELICULAS_API_KEY
    }
    query_params.update(params)

    for k, v in query_params.items():
        conector_query_param = '&' if tiene_query_param(url) else '?'
        url += f'{conector_query_param}{k}={v}'

    return url
