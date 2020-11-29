import json
from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from logic.app.errors.cinema_error import CinemaErrors
from logic.app.errors.discount_error import DiscountErrors
from logic.app.errors.themoviedb_error import TheMovieDBErrors
from logic.app.errors.user_error import UserErrors
from logic.app.models.cinema import Cinema, TimeTablesFilters
from logic.app.models.discount import Discount
from logic.app.models.ticket import CinemaTicket, MovieTicket, Ticket, TicketIn
from logic.app.models.user import DiscountUser, User
from logic.app.repositories import ticket_repository
from logic.app.routes.proxy.v1 import pagina_peliculas_proxy
from logic.app.services import (cinema_service, discount_service,
                                movie_service, qr_service, user_service)
from logic.libs.excepcion.excepcion import AppException


def guardar_ticket(ticket: Ticket) -> UUID:
    return ticket_repository.guardar_ticket(ticket)


def todos_los_ticket() -> List[Ticket]:
    return ticket_repository.todos_los_ticket()


def borrar_ticket(id: UUID) -> Ticket:
    return ticket_repository.borrar_ticket(id)


def buscar_ticket(id: UUID) -> Ticket:
    return ticket_repository.buscar_ticket(id)


def tickets_por_user_id(user_id: UUID) -> List[Ticket]:
    return filter(lambda t: t.user_id == user_id, todos_los_ticket())


def comprar_ticket(ticket_in: TicketIn) -> Ticket:

    dic_themoviedb = movie_service.peliculas_detalle(ticket_in.movie_id)

    movie_ticket = MovieTicket(
        id_themoviedb=ticket_in.movie_id,
        id_poster_img=dic_themoviedb.get('poster_path'),
        name=dic_themoviedb.get('title')
    )

    cinema = cinema_service.buscar_cinema(ticket_in.cinema_id)
    if not cinema:
        msj = f'El cinema con id {str(ticket_in.cinema_id)} no fue encontrado'
        raise AppException(
            codigo=CinemaErrors.CINE_NO_ENCONTRADO, mensaje=msj)

    filters = TimeTablesFilters(movie_id=ticket_in.movie_id,
                                movie_date=ticket_in.movie_date,
                                movie_time=ticket_in.movie_time,
                                room=ticket_in.room)
    cinema_service.ocupar_seats(cinema.id, filters, ticket_in.seats)

    cinema_ticket = CinemaTicket(
        cinema_id=cinema.id,
        name=cinema.name,
        adress=cinema.adress,
        movie_date=ticket_in.movie_date,
        movie_time=ticket_in.movie_time,
        room=ticket_in.room,
        seats=ticket_in.seats
    )

    user = user_service.buscar_user(ticket_in.user_id)

    discounts = []
    for d_id in ticket_in.discounts:

        if DiscountUser(id=d_id) not in user.discounts:
            msj = f'El usuario no tiene el descuento con id {str(d_id)}'
            raise AppException(
                codigo=UserErrors.USUARIO_NO_TIENE_ESE_DESCUENTO, mensaje=msj)

        d = discount_service.buscar_discount(d_id)
        if not d:
            msj = f'El descuento con id {str(d_id)} no fue encontrado'
            raise AppException(
                codigo=DiscountErrors.DESCUENTO_NO_ENCONTRADO, mensaje=msj)

        discounts.append(d)

    price = calcular_precio_final(ticket_in, cinema, discounts)

    id = uuid4()
    ticket = Ticket(
        movie=movie_ticket,
        cinema=cinema_ticket,
        purchase_date=datetime.now(),
        discounts=ticket_in.discounts,
        credit_card_number=ticket_in.credit_card_number,
        price=price,
        user_id=ticket_in.user_id,
        qr=qr_service.crear_qr(id=id),
        id=id
    )

    id_entrada_comprada = ticket_repository.guardar_ticket(ticket)

    for d in discounts:
        user_service.borrar_descuento(ticket_in.user_id, d.id)

    return id_entrada_comprada


def calcular_precio_final(ticket_in: TicketIn, cinema: Cinema = None, discounts: List[Discount] = []) -> float:

    if not cinema:
        cinema = cinema_service.buscar_cinema(ticket_in.cinema_id)

    if not discounts:
        discounts = [
            discount_service.buscar_discount(d.id)
            for d in ticket_in.discounts
        ]

    filters = TimeTablesFilters(movie_id=ticket_in.movie_id,
                                movie_date=ticket_in.movie_date,
                                movie_time=ticket_in.movie_time,
                                room=ticket_in.room)

    try:
        horario = cinema.timetables_por_filters(filters)[0]
    except Exception as e:
        msj = f'El horario con esos filtros no fue encontrado en el cine especificado'
        raise AppException(
            codigo=CinemaErrors.HORARIO_NO_ENCONTRADO, mensaje=msj)

    precio_butaca = cinema.price
    cantidad_butacas = len(ticket_in.seats)

    precio_base = precio_butaca * cantidad_butacas

    descuento_porcentual = 0
    descuento_directo = 0
    for d in discounts:

        if d.discount_percent:
            descuento_porcentual += d.discount_percent / 100
            continue

        if d.discount_price:
            descuento_directo += d.discount_price
            continue

    precio_porcentual = 1 - descuento_porcentual
    precio_final = (precio_base - descuento_directo) * precio_porcentual

    return precio_final
