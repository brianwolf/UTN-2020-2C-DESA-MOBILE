from io import BytesIO
from uuid import UUID, uuid4

from flask import Blueprint, jsonify, render_template, request, send_file
from logic.app.models.user import Login, User
from logic.app.services import cinema_service

blue_print = Blueprint('cinemas', __name__, url_prefix='/api/v1/cinemas')


@blue_print.route('/<id>', methods=['GET'])
def buscar_cinema(id: str):

    cinemas = cinema_service.buscar_cinema(UUID(id))
    if cinemas is None:
        return '', 204

    return jsonify(cinemas.to_json()), 200


@blue_print.route('/', methods=['GET'])
def todos_los_cinema():

    cinemas = cinema_service.todos_los_cinema()
    return jsonify([user.to_json() for user in cinemas]), 200
