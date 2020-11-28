from dataclasses import dataclass, field
from datetime import date, datetime, time
from typing import List
from uuid import UUID, uuid4

from logic.app.models.cinema import Timetable
from logic.app.models.qr import Qr


@dataclass
class TicketIn(object):
    user_id: UUID
    movie_id: int
    cinema_id: UUID
    movie_date: date
    movie_time: time
    room: int
    seats: List[int]
    discounts: List[UUID]
    credit_card_number: str

    def __eq__(self, other):
        return self.id == other.id

    def to_json(self) -> dict:
        return {
            'user_id': str(self.user_id),
            'movie_id': self.movie_id,
            'cinema_id': str(self.cinema_id),
            'movie_date': self.movie_date.isoformat(),
            'movie_time': self.movie_time.isoformat(),
            'room': self.room,
            'seats': self.seats,
            'discounts': [str(d) for d in self.discounts],
            'credit_card_number': self.credit_card_number
        }

    @staticmethod
    def from_json(d: dict) -> 'TicketIn':

        user_id = UUID(d.get('user_id')) if 'user_id' in d else None

        movie_date = date.fromisoformat(
            d.get('movie_date')) if 'movie_date' in d else None

        movie_time = time.fromisoformat(
            d.get('movie_time')) if 'movie_time' in d else None

        room = int(d.get('room')) if 'room' in d else None

        return TicketIn(
            user_id=user_id,
            movie_id=int(d['movie_id']),
            cinema_id=UUID(d['cinema_id']),
            movie_date=movie_date,
            movie_time=movie_time,
            room=room,
            seats=[int(i) for i in d.get('seats', [])],
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
    cinema_id: UUID
    name: str
    adress: str
    movie_date: date
    movie_time: time
    room: int
    seats: List[str]

    def __eq__(self, other):
        return self.cinema_id == other.cinema_id

    def to_json(self) -> dict:
        return {
            'cinema_id': str(self.cinema_id),
            'name': self.name,
            'adress': self.adress,
            'movie_date': self.movie_date.isoformat(),
            'movie_time': self.movie_time.isoformat(),
            'room': self.room,
            'seats': self.seats,
        }

    @staticmethod
    def from_json(d: dict) -> 'CinemaTicket':

        movie_time = time.fromisoformat(
            d.get('movie_time')) if 'movie_time' in d else None

        movie_date = date.fromisoformat(
            d.get('movie_date')) if 'movie_date' in d else None

        room = int(d.get('room')) if 'room' in d else None

        return CinemaTicket(
            cinema_id=UUID(d['cinema_id']),
            name=d['name'],
            adress=d['adress'],
            movie_date=movie_date,
            movie_time=movie_time,
            room=room,
            seats=d['seats']
        )


@dataclass
class Ticket(object):
    movie: MovieTicket
    cinema: CinemaTicket
    purchase_date: datetime
    discounts: List[UUID]
    credit_card_number: str
    price: float
    user_id: UUID
    qr: Qr
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
            'user_id': str(self.user_id),
            'qr': self.qr.to_json(),
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
            user_id=UUID(d['user_id']),
            qr=Qr.from_json(d.get('qr', {})),
            id=id
        )
