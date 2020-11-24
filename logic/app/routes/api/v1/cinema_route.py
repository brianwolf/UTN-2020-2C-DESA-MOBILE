from datetime import time
from io import BytesIO
from uuid import UUID, uuid4

from flask import Blueprint, jsonify, render_template, request, send_file
from logic.app.models.cinema import Location, Place
from logic.app.routes.api.v1.mappers import cinema_mapper
from logic.app.services import cinema_service

blue_print = Blueprint('cinemas', __name__, url_prefix='/api/v1/cinemas')


@blue_print.route('/', methods=['GET'])
def todos_los_cinemas():

    cinemas = cinema_service.todos_los_cinema()
    if cinemas is None:
        return '', 204

    return jsonify([cinema_mapper.cinema_to_json_short(c) for c in cinemas]), 200


@blue_print.route('/<id>', methods=['GET'])
def buscar_cinema(id: str):

    cinema = cinema_service.buscar_cinema(UUID(id))
    if cinema is None:
        return '', 204

    return jsonify(cinema_mapper.cinema_to_json_short(cinema)), 200


@blue_print.route('/closest', methods=['GET'])
def todos_los_cinema_mas_cercano():

    longitude = float(request.args.get('longitude'))
    latitude = float(request.args.get('latitude'))

    location = Location(longitude=longitude, latitude=latitude)

    json_cinemas = []
    for c in cinema_service.todos_los_cinema_mas_cercano(location):

        j = c.to_json()
        j.pop('location')
        j.pop('image_path')
        j.pop('timetables')

        json_cinemas.append(j)

    return jsonify(json_cinemas), 200


@blue_print.route('/<id>/full', methods=['GET'])
def buscar_cinema_full(id: str):

    cinemas = cinema_service.buscar_cinema(UUID(id))
    if cinemas is None:
        return '', 204

    return jsonify(cinemas.to_json()), 200


@blue_print.route('/full', methods=['GET'])
def todos_los_cinema_full():

    cinemas = cinema_service.todos_los_cinema()
    return jsonify([user.to_json() for user in cinemas]), 200


@blue_print.route('/<id>/img', methods=['GET'])
def buscar_cinema_imgagen(id: str):

    cinema = cinema_service.buscar_cinema(UUID(id))

    if cinema is None:
        return '', 204

    return send_file(BytesIO(cinema.cargar_contenido()),
                     mimetype='image/jpeg',
                     as_attachment=True,
                     attachment_filename=str(cinema.id))


@blue_print.route('/<id>/timetables', methods=['GET'])
def buscar_cinema_timetables(id: str):

    cinemas = cinema_service.buscar_cinema(UUID(id))
    if cinemas is None:
        return '', 204

    result = [t.to_json() for t in cinemas.timetables]
    result = [t.pop('movie_time') for t in result]

    return jsonify(result), 200


@blue_print.route('/<id>/timetables/<movie_time>/places', methods=['GET'])
def buscar_cinema_places(id: str, movie_time: str):

    cinemas = cinema_service.buscar_cinema(UUID(id))
    if cinemas is None:
        return '', 204

    places = []
    for t in cinemas.timetables:
        if t.movie_time == time.fromisoformat(movie_time):
            places = t.places

    if not places:
        return '', 204

    result = [r.to_json() for r in places]
    return jsonify(result), 200


@blue_print.route('/<id>/timetables/<movie_time>/places/enables', methods=['GET'])
def buscar_cinema_places_enables(id: str, movie_time: str):

    cinemas = cinema_service.buscar_cinema(UUID(id))
    if cinemas is None:
        return '', 204

    places = []
    for t in cinemas.timetables:
        if t.movie_time == time.fromisoformat(movie_time):
            places = t.places

    if not places:
        return '', 204

    result = [r.to_json().pop('name') for r in places if r.enable]
    return jsonify(result), 200
