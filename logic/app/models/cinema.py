from dataclasses import dataclass, field
from datetime import datetime, time
from typing import List
from uuid import UUID, uuid4


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
    enable: bool

    def __eq__(self, other):
        return self.name == other.name

    def to_json(self) -> dict:
        return self.__dict__.copy()

    @staticmethod
    def from_json(d: dict) -> 'Place':
        return Place(**d)


@dataclass
class Timetable(object):
    movie_time: time
    places: List[Place]

    def __eq__(self, other):
        return self.movie_time == other.movie_time

    def to_json(self) -> dict:
        return {
            'movie_time': self.movie_time.isoformat(),
            'places': [o.to_json() for o in self.places]
        }

    @staticmethod
    def from_json(d: dict) -> 'Timetable':

        movie_time = time.fromisoformat(
            d.get('movie_time')) if 'movie_time' in d else datetime.now().time()

        return Timetable(
            movie_time=movie_time,
            places=[Place.from_json(d) for d in d.get('places')]
        )


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
