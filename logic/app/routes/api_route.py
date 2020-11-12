import ntpath
from io import BytesIO
from os import listdir, getcwd

from flask import Blueprint, jsonify, render_template, send_file
from logic.app.configs import config, directorios_config
from logic.app.repositories import (cinema_repository, discount_repository,
                                    qr_repository, user_repository)

blue_print = Blueprint('api', __name__, url_prefix='')


@blue_print.route('/variables')
def variables():
    return jsonify({
        key: value for key, value
        in config.__dict__.items()
        if not str(key).startswith('_')
    })


@blue_print.route('/')
def vivo():
    return jsonify({"estado": "vivo"})


@blue_print.route('/db/reiniciar', methods=['DELETE'])
def borrar_directorios_generados():

    directorios_config.borrar_directorios()
    directorios_config.iniciar_directorios()

    cinema_repository._cargar_db()
    discount_repository._cargar_db()
    qr_repository._cargar_db()
    user_repository._cargar_db()

    return '', 200


@blue_print.route('/postman', methods=['GET'])
def descargar_coleccion_de_postman():

    archivo_dir = next(iter([
        f
        for f in listdir(getcwd())
        if str(f).endswith('.postman_collection.json')
    ]), None)

    if not archivo_dir:
        return '', 204

    return send_file(BytesIO(open(archivo_dir, 'rb').read()),
                     mimetype='application/octet-stream',
                     as_attachment=True,
                     attachment_filename=ntpath.basename(archivo_dir))
