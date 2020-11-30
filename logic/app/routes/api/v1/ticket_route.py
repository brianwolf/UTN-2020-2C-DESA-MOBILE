from datetime import time
from io import BytesIO
from uuid import UUID, uuid4

from flask import Blueprint, Request, jsonify, request
from logic.app.models.ticket import Ticket, TicketIn
from logic.app.models.user import DiscountUser, User
from logic.app.routes.api.v1.mappers import ticket_mapper
from logic.app.services import ticket_service, user_service

blue_print = Blueprint('tickets', __name__, url_prefix='/api/v1/tickets')


def _user_logueado() -> User:
    token = request.args.get('token')
    if not token:
        return None

    return user_service.buscar_user_logueado(UUID(token))


@blue_print.route('/', methods=['GET'])
def todos_los_ticket():

    tickets = ticket_service.todos_los_ticket()
    if tickets is None:
        return '', 204

    return jsonify([ticket_mapper.ticket_to_json(o) for o in tickets]), 200


@blue_print.route('/byToken', methods=['GET'])
def tickets_del_user():

    user = _user_logueado()
    if not user:
        return 'Usuario no logueado', 403

    tickets = ticket_service.tickets_por_user_id(user.id)
    if tickets is None:
        return '', 204

    return jsonify([ticket_mapper.ticket_to_json(o) for o in tickets]), 200


@blue_print.route('/price/byToken', methods=['POST'])
def calcular_precio_compra():

    user = _user_logueado()
    if not user:
        return 'Usuario no logueado', 403

    ticket = TicketIn.from_json(request.json)
    ticket.user_id = user.id
    ticket.discounts = [du.id for du in user.discounts]

    precio = ticket_service.calcular_precio_final(ticket)
    return jsonify(price=precio), 200


@blue_print.route('/byToken', methods=['POST'])
def comprar_ticket():

    user = _user_logueado()
    if not user:
        return 'Usuario no logueado', 403

    ticket = TicketIn.from_json(request.json)
    ticket.user_id = user.id
    ticket.discounts = [du.id for du in user.discounts]

    id_ticket = ticket_service.comprar_ticket(ticket)
    return jsonify(id=id_ticket), 201
