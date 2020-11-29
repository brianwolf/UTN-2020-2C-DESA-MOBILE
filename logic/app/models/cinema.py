from dataclasses import dataclass, field
from datetime import date, datetime, time
from typing import List
from uuid import UUID, uuid4

from logic.app.errors.cinema_error import CinemaErrors
from logic.libs.excepcion.excepcion import AppException


@dataclass
class Location(object):
    latitude: float
    longitude: float

    def __eq__(self, other):
        return self.latitude == other.latitude and self.longitude == other.longitude

    def to_json(self) -> dict:
        return self.__dict__.copy()

    @staticmethod
    def from_json(d: dict) -> 'Location':
        return Location(**d)


@dataclass
class Seat(object):
    id: int = None
    enable: bool = True

    def __eq__(self, other):
        return self.name == other.name

    def to_json(self) -> dict:
        return self.__dict__.copy()

    @staticmethod
    def from_json(d: dict) -> 'Seat':

        id = int(d.get('id')) if 'id' in d else None

        return Seat(
            id=id,
            enable=bool(d.get('enable', True))
        )


@dataclass
class Timetable(object):
    movie_id: int
    movie_date: date
    movie_time: time
    room: int
    seats: List[Seat]
    price: float = 0

    def __eq__(self, other):
        return self.movie_time == other.movie_time and self.movie_id == other.movie_id and self.movie_date == other.movie_date

    def to_json(self) -> dict:
        return {
            'movie_id': self.movie_id,
            'movie_date': self.movie_date.isoformat(),
            'movie_time': self.movie_time.isoformat(),
            'seats': [o.to_json() for o in self.seats],
            'price': str(self.price),
            'room': self.room
        }

    @staticmethod
    def from_json(d: dict) -> 'Timetable':

        movie_time = time.fromisoformat(
            d.get('movie_time')) if 'movie_time' in d else datetime.now().time()

        movie_date = date.fromisoformat(
            d.get('movie_date')) if 'movie_date' in d else datetime.now().date()

        return Timetable(
            movie_id=d.get('movie_id'),
            movie_date=movie_date,
            movie_time=movie_time,
            seats=[Seat.from_json(d) for d in d.get('seats')],
            price=float(d.get('price', 0)),
            room=int(d.get('room', 0))
        )

    def ocupar_seat(self, seat_id: int):

        butacas_elegidas = list(
            filter(lambda p: p.id == seat_id, self.seats))

        butacas_elegidas_ocupadas = [
            p for p in butacas_elegidas
            if not p.enable
        ]
        if butacas_elegidas_ocupadas:
            msj = f'La butaca {seat_id} esta ocupada'
            raise AppException(codigo=CinemaErrors.BUTACA_OCUPADA, mensaje=msj)

        for p in butacas_elegidas:
            p.enable = False


@dataclass
class TimeTablesFilters(object):
    movie_id: int = None
    movie_date: date = None
    movie_time: date = None
    room: int = None

    def to_json(self) -> dict:
        return {
            'movie_id': self.movie_id,
            'movie_date': self.movie_date.isoformat if self.movie_date else None,
            'movie_time': self.movie_time.isoformat if self.movie_time else None,
            'room': self.room if self.room else None,
        }

    @staticmethod
    def from_json(d: dict) -> 'TimeTablesFilters':

        movie_id = int(d.get('movie_id')) if 'movie_id' in d else None

        movie_date = date.fromisoformat(
            d.get('movie_date')) if 'movie_date' in d else None

        movie_time = time.fromisoformat(
            d.get('movie_time')) if 'movie_time' in d else None

        room = int(d.get('room')) if 'room' in d else None

        return TimeTablesFilters(
            movie_id=movie_id,
            movie_date=movie_date,
            movie_time=movie_time,
            room=room
        )


@dataclass
class Cinema(object):
    name: str = None
    adress: str = None
    description: str = None
    stars: float = None
    location: Location = None
    image_path: str = None
    timetables: List[Timetable] = None
    id: UUID = field(default_factory=uuid4)
    price: float = None

    def __eq__(self, other):
        return self.id == other.id

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'description': self.description,
            'adress': self.adress,
            'stars': self.stars,
            'location': self.location.to_json(),
            'image_path': self.image_path,
            'timetables': [o.to_json() for o in self.timetables],
            'id': str(self.id),
            'price': str(self.price)
        }

    @staticmethod
    def from_json(d: dict) -> 'Cinema':

        id = UUID(str(d.get('id'))) if 'id' in d else uuid4()

        return Cinema(
            name=d.get('name'),
            description=d.get('description'),
            adress=d.get('adress'),
            stars=float(d.get('stars')),
            location=Location.from_json(d.get('location')),
            image_path=d.get('image_path'),
            timetables=[Timetable.from_json(d) for d in d.get('timetables')],
            id=id,
            price=float(d.get('price')) if 'price' in d else None
        )

    def cargar_contenido(self) -> bytes:
        with open(self.image_path, 'rb') as archivo:
            return archivo.read()

    def timetables_por_filters(self, filters: TimeTablesFilters = TimeTablesFilters()) -> List[Timetable]:

        resultado = self.timetables

        if filters.movie_id:
            resultado = filter(lambda tt: tt.movie_id ==
                               filters.movie_id, resultado)

        if filters.movie_date:
            resultado = filter(lambda tt: tt.movie_date ==
                               filters.movie_date, resultado)

        if filters.movie_time:
            resultado = filter(lambda tt: tt.movie_time ==
                               filters.movie_time, resultado)

        if filters.room:
            resultado = filter(lambda tt: tt.room ==
                               filters.room, resultado)

        return list(resultado)
