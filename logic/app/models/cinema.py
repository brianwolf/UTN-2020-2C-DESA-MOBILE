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
class Place(object):
    name: str
    enable: bool = True

    def __eq__(self, other):
        return self.name == other.name

    def to_json(self) -> dict:
        return self.__dict__.copy()

    @staticmethod
    def from_json(d: dict) -> 'Place':
        return Place(
            name=d.get('name'),
            enable=bool(d.get('enable', True))
        )


@dataclass
class Timetable(object):
    movie_id: int
    movie_date: date
    movie_time: time
    places: List[Place]
    price: float = 0

    def __eq__(self, other):
        return self.movie_time == other.movie_time and self.movie_id == other.movie_id and self.movie_date == other.movie_date

    def to_json(self) -> dict:
        return {
            'movie_id': self.movie_id,
            'movie_date': self.movie_date.isoformat(),
            'movie_time': self.movie_time.isoformat(),
            'places': [o.to_json() for o in self.places],
            'price': str(self.price)
        }

    @staticmethod
    def from_json(d: dict) -> 'Timetable':

        movie_time = time.fromisoformat(
            d.get('movie_time')) if 'movie_time' in d else datetime.now().time()

        movie_date = time.fromisoformat(
            d.get('movie_date')) if 'movie_date' in d else datetime.now().date()

        return Timetable(
            movie_id=d.get('movie_id'),
            movie_date=movie_date,
            movie_time=movie_time,
            places=[Place.from_json(d) for d in d.get('places')],
            price=float(d.get('price', 0))
        )

    def ocupar_place(self, place_name: str):

        butacas_elegidas = list(
            filter(lambda p: p.name == place_name, self.places))

        butacas_elegidas_ocupadas = [
            p for p in butacas_elegidas
            if not p.enable
        ]
        if butacas_elegidas_ocupadas:
            msj = f'La butaca {place_name} esta ocupada'
            raise AppException(codigo=CinemaErrors.BUTACA_OCUPADA, mensaje=msj)

        for p in butacas_elegidas:
            p.enable = False


@dataclass
class Cinema(object):
    name: str
    adress: str
    description: str
    stars: float
    location: Location
    image_path: str
    timetables: List[Timetable]
    id: UUID = field(default_factory=uuid4)

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
            'id': str(self.id)
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
            id=id
        )

    def cargar_contenido(self) -> bytes:
        with open(self.image_path, 'rb') as archivo:
            return archivo.read()

    def buscar_time_table(self, movie_time: time) -> Timetable:
        resultado = list(filter(lambda tt: tt.movie_time ==
                                movie_time, self.timetables))
        return resultado[0] if resultado else None
