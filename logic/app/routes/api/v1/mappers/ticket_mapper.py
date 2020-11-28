from logic.app.models.ticket import Ticket
from logic.app.routes.api.v1.mappers import qr_mapper


def ticket_to_json(ticket: Ticket) -> dict:

    j = ticket.to_json()
    j['qr'] = qr_mapper.qr_to_json(ticket.qr)
    return j
