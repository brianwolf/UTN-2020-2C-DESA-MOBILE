from io import BytesIO
from uuid import uuid4, UUID

from flask import Blueprint, jsonify, render_template, send_file
from logic.app.services import qr_service

blue_print = Blueprint('qr', __name__, url_prefix='/api/v1/qr')


@blue_print.route('/', methods=['POST'])
def crear_qr():

    qr = qr_service.crear_qr()
    return jsonify(qr.to_json()), 201


@blue_print.route('/<id>', methods=['GET'])
def buscar_qr(id: str):

    qr = qr_service.buscar_qr(UUID(id))
    if qr is None:
        return '', 204

    return send_file(BytesIO(qr.cargar_contenido()),
                     mimetype='image/jpeg',
                     as_attachment=True,
                     attachment_filename=str(qr.id))


@blue_print.route('/', methods=['GET'])
def todos_los_qr():

    qrs = qr_service.todos_los_qr()
    return jsonify([qr.to_json() for qr in qrs]), 200


@blue_print.route('/<id>', methods=['DELETE'])
def borrar_qr(id: str):

    qr = qr_service.borrar_qr(UUID(id))
    if qr is None:
        return '', 204

    return '', 200
