from flask import Blueprint, jsonify, render_template

from logic.app.configs import config

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
