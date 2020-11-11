from io import BytesIO
from uuid import UUID, uuid4

from flask import Blueprint, jsonify, render_template, request, send_file
from logic.app.models.user import Login, User
from logic.app.services import user_service

blue_print = Blueprint('users', __name__, url_prefix='/api/v1/users')


@blue_print.route('/login', methods=['POST'])
def loguearse():

    token = user_service.login_user(Login.from_json(request.json))
    if token is None:
        return '', 204

    return jsonify(token=token), 200


@blue_print.route('/', methods=['POST'])
def crear_user():

    id = user_service.guardar_user(User.from_json(request.json))
    return jsonify(id=id), 201


@blue_print.route('/<id>', methods=['GET'])
def buscar_user(id: str):

    user = user_service.buscar_user(UUID(id))
    if user is None:
        return '', 204

    return jsonify(user.to_json()), 200


@blue_print.route('/', methods=['GET'])
def todos_los_user():

    users = user_service.todos_los_user()
    return jsonify([user.to_json() for user in users]), 200


@blue_print.route('/<id>', methods=['DELETE'])
def borrar_user(id: str):

    user = user_service.borrar_user(UUID(id))
    if user is None:
        return '', 204

    return '', 200
