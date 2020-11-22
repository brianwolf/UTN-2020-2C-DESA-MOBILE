import json
from datetime import datetime
from typing import List
from uuid import UUID

from logic.app.models.cinema import Cinema
from logic.app.models.discount import Discount
from logic.app.models.ticket import CinemaTicket, MovieTicket, Ticket, TicketIn
from logic.app.models.user import User
from logic.app.repositories import ticket_repository
from logic.app.routes.proxy.v1 import pagina_peliculas_proxy
from logic.app.services import cinema_service, discount_service, qr_service


def guardar_ticket(ticket: Ticket) -> UUID:
    return ticket_repository.guardar_ticket(ticket)


def todos_los_ticket() -> List[Ticket]:
    return ticket_repository.todos_los_ticket()


def borrar_ticket(id: UUID) -> Ticket:
    return ticket_repository.borrar_ticket(id)


def buscar_ticket(id: UUID) -> Ticket:
    return ticket_repository.buscar_ticket(id)


def buscar_ticket_por_user(user: User) -> List[Ticket]:

    tickets = todos_los_ticket()

    return list(filter(lambda t: t.id_user == user.id, tickets))


def comprar_ticket(ticket_in: TicketIn) -> Ticket:

    qr = qr_service.crear_qr()

    url_final = f'/movie/{ticket_in.id_movie}'
    respuesta = pagina_peliculas_proxy.proxy(url_final)
    dic_themoviedb = json.loads(respuesta.decode('utf-8'))

    movie_ticket = MovieTicket(
        id_themoviedb=ticket_in.id_movie,
        id_poster_img=dic_themoviedb.get('poster_path'),
        name=dic_themoviedb.get('title')
    )

    cinema = cinema_service.buscar_cinema(ticket_in.id_cinema)
    cinema_service.ocupar_places(cinema.id, ticket_in.places)

    cinema_ticket = CinemaTicket(
        id_cinema=cinema.id,
        name=cinema.name,
        adress=cinema.adress,
        movie_time=ticket_in.movie_time,
        places=ticket_in.places
    )

    discounts = [
        discount_service.buscar_discount(d.id)
        for d in ticket_in.discounts
    ]

    price = calcular_precio_final(
        ticket_in=ticket_in, cinema=cinema, discounts=discounts)

    ticket = Ticket(
        movie=movie_ticket,
        cinema=cinema_ticket,
        purchase_date=datetime.now(),
        discounts=ticket_in.discounts,
        credit_card_number=ticket_in.credit_card_number,
        price=price,
        id_user=ticket_in.id_user,
        id_qr=qr.id
    )

    return ticket_repository.guardar_ticket(ticket)


def calcular_precio_final(ticket_in: TicketIn, cinema: Cinema = None, discounts: List[Discount] = []) -> float:

    if not cinema:
        cinema = cinema_service.buscar_cinema(ticket_in.id_cinema)

    if not discounts:
        discounts = [
            discount_service.buscar_discount(d.id)
            for d in ticket_in.discounts
        ]

    precio_butaca = cinema.buscar_time_table(ticket_in.movie_time).price
    cantidad_butacas = len(ticket_in.places)

    precio_base = precio_butaca * cantidad_butacas

    descuento_porcentual = 0
    descuento_directo = 0
    for d in discounts:

        if d.discount_percent:
            descuento_porcentual += d.discount_percent / 100
            continue

        if d.descuento_directo:
            descuento_directo += d.descuento_directo
            continue

    precio_porcentual = 1 - descuento_porcentual
    precio_final = (precio_base - descuento_directo) * precio_porcentual

    return precio_final
