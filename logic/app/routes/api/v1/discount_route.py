from datetime import time
from io import BytesIO
from uuid import UUID, uuid4

from flask import (Blueprint, Request, jsonify, render_template, request,
                   send_file)
from logic.app.models.cinema import Seat
from logic.app.models.user import DiscountUser, User
from logic.app.routes.api.v1.mappers import discount_mapper
from logic.app.services import discount_service, user_service

blue_print = Blueprint('discounts', __name__, url_prefix='/api/v1/discounts')


def _user_logueado() -> User:
    token = request.args.get('token')
    if not token:
        return None

    return user_service.buscar_user_logueado(UUID(token))


@blue_print.route('/', methods=['GET'])
def todos_los_discount():

    discounts = discount_service.todos_los_discount()
    if discounts is None:
        return '', 204

    return jsonify([discount_mapper.discount_to_json(o) for o in discounts]), 200


@blue_print.route('/byToken', methods=['GET'])
def discounts_del_user():

    user = _user_logueado()
    if not user:
        return 'Usuario no logueado', 403

    discounts = discount_service.buscar_discount_por_user(user)
    if discounts is None:
        return '', 204

    return jsonify([discount_mapper.discount_to_json(o) for o in discounts]), 200


@blue_print.route('/byToken', methods=['POST'])
def agregar_discounts_al_user():

    user = _user_logueado()
    if not user:
        return 'Usuario no logueado', 403

    discount_user = DiscountUser.from_json(request.json)

    discount_service.agregar_discount_a_user(user, discount_user)
    return '', 200
