from flask import Blueprint, jsonify, render_template
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
