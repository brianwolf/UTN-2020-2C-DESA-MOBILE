from datetime import date, time
from io import BytesIO
from uuid import UUID, uuid4

from flask import Blueprint, jsonify, render_template, request, send_file
from logic.app.models.cinema import TimeTablesFilters, Location, Seat
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


@blue_print.route('/closest/latitude/<latitude>/longitude/<longitude>', methods=['GET'])
def todos_los_cinema_mas_cercano(latitude: str, longitude: str):

    filters = TimeTablesFilters.from_json(request.args)

    location = Location(longitude=float(longitude), latitude=float(latitude))

    cinemas = cinema_service.todos_los_cinema_mas_cercano(
        location, filters=filters)

    return jsonify([cinema_mapper.cinema_to_json_short(c) for c in cinemas]), 200


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

    filters = TimeTablesFilters.from_json(request.args)

    cinema = cinema_service.buscar_cinema(UUID(id))
    if cinema is None:
        return '', 204

    return jsonify([t.to_json() for t in cinema.timetables_por_filters(filters)]), 200


@blue_print.route('/<id>/timetables/seats', methods=['GET'])
def buscar_cinema_timetables_seats(id: str):

    filters = TimeTablesFilters.from_json(request.args)

    cinema = cinema_service.buscar_cinema(UUID(id))
    if cinema is None:
        return '', 204

    seats = [
        t.seats
        for t in cinema.timetables_por_filters(filters)]

    return jsonify(seats), 200


@blue_print.route('/<id>/dates', methods=['GET'])
def buscar_cinema_dates(id: str):

    filters = TimeTablesFilters.from_json(request.args)

    cinema = cinema_service.buscar_cinema(UUID(id))
    if cinema is None:
        return '', 204

    dates = [
        tt.movie_date
        for tt in cinema.timetables_por_filters(filters)
    ]

    return jsonify(set(dates)), 200


@blue_print.route('/<id>/times', methods=['GET'])
def buscar_cinema_times(id: str):

    filters = TimeTablesFilters.from_json(request.args)

    cinema = cinema_service.buscar_cinema(UUID(id))
    if cinema is None:
        return '', 204

    times = [
        str(tt.movie_time)
        for tt in cinema.timetables_por_filters(filters)
    ]

    return jsonify(set(times)), 200


@blue_print.route('/<id>/rooms', methods=['GET'])
def buscar_cinema_rooms(id: str):

    filters = TimeTablesFilters.from_json(request.args)

    cinema = cinema_service.buscar_cinema(UUID(id))
    if cinema is None:
        return '', 204

    list_room = [
        tt.room
        for tt in cinema.timetables_por_filters(filters)
    ]

    return jsonify(set(list_room)), 200


@blue_print.route('/<id>/seats/enables/ids', methods=['GET'])
def buscar_cinema_timetables_seats_enables(id: str):

    filters = TimeTablesFilters.from_json(request.args)

    cinema = cinema_service.buscar_cinema(UUID(id))
    if cinema is None:
        return '', 204

    list_seats = [
        tt.seats
        for tt in cinema.timetables_por_filters(filters)
    ]

    ids = [
        s.id
        for s in sum(list_seats, [])
        if s.enable
    ]

    return jsonify(ids), 200
