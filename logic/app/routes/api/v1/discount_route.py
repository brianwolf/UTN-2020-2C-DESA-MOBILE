from datetime import time
from io import BytesIO
from uuid import UUID, uuid4

from flask import Blueprint, jsonify, render_template, request, send_file
from logic.app.models.cinema import Place
from logic.app.models.user import User
from logic.app.routes.api.v1.mappers import discount_mapper
from logic.app.services import discount_service, user_service

blue_print = Blueprint('discounts', __name__, url_prefix='/api/v1/discounts')


def _user_logueado() -> User:

    token = request.params.get('token')
    if token is None:
        return 'Se debe enviar el token por query param', 403

    user = user_service.buscar_user_logueado(UUID(token))
    if token is None:
        return 'Usuario no encontrado', 403

    return user


@blue_print.route('/', methods=['GET'])
def todos_los_discount():

    discounts = discount_service.todos_los_discount()
    if discounts is None:
        return '', 204

    return jsonify([discount_mapper.discount_to_json(o) for o in discounts]), 200


@blue_print.route('/byToken', methods=['GET'])
def discounts_from_user():

    user = _user_logueado()

    discounts = discount_service.buscar_discount_por_user(user)
    if discounts is None:
        return '', 204

    return jsonify([discount_mapper.discount_to_json(o) for o in discounts]), 200
