from flask import Blueprint, jsonify, render_template, request
from logic.app.configs import config
from logic.libs.logger.logger import log
from pip._vendor.requests import get

blue_print = Blueprint('pagina_peliculas', __name__,
                       url_prefix='/proxy/v1/themoviedb')


@blue_print.route('/<path:path>', methods=['GET'])
def proxy(path):

    host = config.PAG_PELICULAS_URL

    query_param_api_key = f'api_key={config.PAG_PELICULAS_API_KEY}'
    query_param_idioma = f'language={config.PAG_PELICULAS_IDIOMA}'

    url_final = f'{host}{path}?{query_param_api_key}&{query_param_idioma}'
    log().info(f'URL a redireccionar -> {url_final}')

    respuesta = get(url_final)
    try:
        return jsonify(respuesta.json())

    except Exception as e:
        return respuesta.content
