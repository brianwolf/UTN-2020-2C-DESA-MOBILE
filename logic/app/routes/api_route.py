from flask import Blueprint, jsonify, render_template

from logic.app.configs import config

blue_print = Blueprint('api', __name__, url_prefix='')


@blue_print.route('/variables')
def variables():
    return jsonify(config.__dict__())


@blue_print.route('/vivo')
def vivo():
    return jsonify({"estado": "vivo"})
