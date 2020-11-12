import io
import os
import requests

from flask import Blueprint, send_file
from logic.app.configs import config
from logic.libs.logger.logger import log

blue_print = Blueprint('pagina_imagenes', __name__,
                       url_prefix='/proxy/v1/imagetmdb')


@blue_print.route('/<path:path>', methods=['GET'])
def proxy(path: str):

    url_final = os.path.join(config.PAG_IMAGENES_URL, path)

    log().info(f'URL a redireccionar -> {url_final}')

    respuesta = requests.get(url_final)

    nombre_imagen = path.replace('/', '')
    return send_file(
        io.BytesIO(respuesta.content),
        mimetype='image/jpeg',
        as_attachment=False,
        attachment_filename=nombre_imagen)
