from datetime import time
from io import BytesIO
from uuid import UUID, uuid4

from flask import (Blueprint, Request, jsonify, render_template, request,
                   send_file)
from logic.app.models.ticket import Ticket, TicketIn
from logic.app.models.user import DiscountUser, User
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

    return jsonify([o.to_json() for o in tickets]), 200


@blue_print.route('/byToken', methods=['GET'])
def tickets_del_user():

    user = _user_logueado()
    if not user:
        return 'Usuario no logueado', 403

    tickets = ticket_service.buscar_ticket_por_user(user)
    if tickets is None:
        return '', 204

    return jsonify([o.to_json() for o in tickets]), 200


@blue_print.route('/byToken', methods=['POST'])
def comprar_ticket():

    user = _user_logueado()
    if not user:
        return 'Usuario no logueado', 403

    ticket = TicketIn.from_json(request.json)
    ticket.id_user = user.id

    id_ticket = ticket_service.comprar_ticket(ticket)
    return jsonify(id=id_ticket), 201
