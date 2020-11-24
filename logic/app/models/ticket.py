from dataclasses import dataclass, field
from datetime import datetime, time
from typing import List
from uuid import UUID, uuid4

from logic.app.models.cinema import Timetable


@dataclass
class TicketIn(object):
    id_user: UUID
    id_movie: int
    id_cinema: UUID
    movie_time: time
    places: List[str]
    discounts: List[UUID]
    credit_card_number: str

    def __eq__(self, other):
        return self.id == other.id

    def to_json(self) -> dict:
        return {
            'id_user': str(self.id_user),
            'id_movie': self.id_movie,
            'id_cinema': str(self.id_cinema),
            'movie_time': self.movie_time.isoformat(),
            'places': self.places,
            'discounts': [str(d) for d in self.discounts],
            'credit_card_number': self.credit_card_number
        }

    @staticmethod
    def from_json(d: dict) -> 'TicketIn':

        id_user = UUID(d.get('id_user')) if 'id_user' in d else None

        movie_time = time.fromisoformat(
            d.get('movie_time')) if 'movie_time' in d else datetime.now().time()

        return TicketIn(
            id_user=id_user,
            id_movie=int(d['id_movie']),
            id_cinema=UUID(d['id_cinema']),
            movie_time=movie_time,
            places=d['places'],
            discounts=[UUID(u) for u in d.get('discounts', [])],
            credit_card_number=d['credit_card_number']
        )


@dataclass
class MovieTicket(object):
    id_themoviedb: str
    id_poster_img: str
    name: str

    def __eq__(self, other):
        return self.id_themoviedb == other.id_themoviedb

    def to_json(self) -> dict:
        return {
            'id_themoviedb': self.id_themoviedb,
            'id_poster_img': self.id_poster_img,
            'name': self.name
        }

    @staticmethod
    def from_json(d: dict) -> 'MovieTicket':

        return MovieTicket(
            id_themoviedb=d['id_themoviedb'],
            id_poster_img=d['id_poster_img'],
            name=d['name']
        )


@dataclass
class CinemaTicket(object):
    id_cinema: UUID
    name: str
    adress: str
    movie_time: time
    places: List[str]

    def __eq__(self, other):
        return self.id_cinema == other.id_cinema

    def to_json(self) -> dict:
        return {
            'id_cinema': str(self.id_cinema),
            'name': self.name,
            'adress': self.adress,
            'movie_time': self.movie_time.isoformat(),
            'places': self.places,
        }

    @staticmethod
    def from_json(d: dict) -> 'CinemaTicket':

        movie_time = time.fromisoformat(
            d.get('movie_time')) if 'movie_time' in d else datetime.now().time()

        return CinemaTicket(
            id_cinema=UUID(d['id_cinema']),
            name=d['name'],
            adress=d['adress'],
            movie_time=movie_time,
            places=d['places']
        )


@dataclass
class Ticket(object):
    movie: MovieTicket
    cinema: CinemaTicket
    purchase_date: datetime
    discounts: List[UUID]
    credit_card_number: str
    price: float
    id_user: UUID
    id_qr: UUID
    id: UUID = field(default_factory=uuid4)

    def __eq__(self, other):
        return self.id == other.id

    def to_json(self) -> dict:
        return {
            'movie': self.movie.to_json(),
            'cinema': self.cinema.to_json(),
            'purchase_date': self.purchase_date.isoformat(),
            'discounts': [str(d) for d in self.discounts],
            'credit_card_number': self.credit_card_number,
            'price': str(self.price),
            'id_user': str(self.id_user),
            'id_qr': str(self.id_qr),
            'id': str(self.id)
        }

    @staticmethod
    def from_json(d: dict) -> 'Ticket':

        id = UUID(str(d.get('id'))) if 'id' in d else uuid4()

        return Ticket(
            movie=MovieTicket.from_json(d['movie']),
            cinema=CinemaTicket.from_json(d['cinema']),
            purchase_date=datetime.fromisoformat(d['purchase_date']),
            discounts=[UUID(u) for u in d['discounts']],
            credit_card_number=d['credit_card_number'],
            price=float(d['price']),
            id_user=UUID(d['id_user']),
            id_qr=UUID(d['id_qr']),
            id=id
        )
