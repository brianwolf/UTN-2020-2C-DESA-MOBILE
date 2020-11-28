from dataclasses import dataclass, field
from typing import List
from uuid import UUID, uuid4

from logic.app.models.cinema import Timetable


@dataclass
class TicketIn(object):
    id_user: UUID
    id_cinema: UUID
    movie_time: str
    seats: List[str]
    discounts: List[UUID]
    credit_card_number: str

    def __eq__(self, other):
        return self.id == other.id

    def to_json(self) -> dict:
        return {
            'id_user': str(self.id_user),
            'id_cinema': str(self.id_cinema),
            'movie_time': self.movie_time,
            'seats': self.seats,
            'discounts': [str(d) for d in self.discounts],
            'credit_card_number': self.credit_card_number
        }

    @staticmethod
    def from_json(d: dict) -> 'TicketIn':

        return TicketIn(
            id_user=UUID(d['id_user']),
            id_cinema=UUID(d['id_cinema']),
            movie_time=d['movie_time'],
            palces=d['seats'],
            discounts=[UUID(u) for u in d['discounts']],
            credit_card_number=d['credit_card_number']
        )


@dataclass
class TicketOut(object):
    id_user: UUID
    id_cinema: UUID
    movie_time: str
    seats: List[str]
    discounts: List[UUID]
    credit_card_number: str

    def __eq__(self, other):
        return self.id == other.id

    def to_json(self) -> dict:
        return {
            'id_user': str(self.id_user),
            'id_cinema': str(self.id_cinema),
            'movie_time': self.movie_time,
            'seats': self.seats,
            'discounts': [str(d) for d in self.discounts],
            'credit_card_number': self.credit_card_number
        }

    @staticmethod
    def from_json(d: dict) -> 'TicketIn':

        return TicketIn(
            id_user=UUID(d['id_user']),
            id_cinema=UUID(d['id_cinema']),
            movie_time=d['movie_time'],
            palces=d['seats'],
            discounts=[UUID(u) for u in d['discounts']],
            credit_card_number=d['credit_card_number']
        )
