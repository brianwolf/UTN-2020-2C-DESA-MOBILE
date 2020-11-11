from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from uuid import UUID, uuid4


@dataclass
class Login(object):
    user: str
    password: str

    def __eq__(self, other):
        return self.user == other.user and self.password == other.password

    def to_json(self) -> dict:
        return self.__dict__

    @staticmethod
    def from_json(d: dict) -> 'Login':
        return Login(**d)


@dataclass
class CreditCard(object):
    number: str
    name: str
    expiration: str

    def __eq__(self, other):
        return self.number == other.number

    def to_json(self) -> dict:
        return self.__dict__

    @staticmethod
    def from_json(d: dict) -> 'CreditCard':
        return CreditCard(**d)


@dataclass
class User(object):
    login: Login
    creditCars: List[CreditCard] = field(default_factory=list)
    last_conection: datetime = datetime.now()
    id: UUID = uuid4()

    def __eq__(self, other):
        return self.id == other.id

    def to_json(self) -> dict:
        return {
            'id': str(self.id),
            'last_conection': self.last_conection.isoformat(),
            'creditCars': [cc.to_json() for cc in self.creditCars],
            'login': self.login.to_json()
        }

    @staticmethod
    def from_json(d: dict) -> 'Qr':

        id = UUID(str(d.get('id'))) if 'id' in d else uuid4()

        last_conection = datetime.fromisoformat(
            d.get('last_conection')) if 'last_conection' in d else datetime.now()

        return User(
            login=Login.from_json(d['login']),
            id=id,
            last_conection=last_conection,
            creditCars=[CreditCard.from_json(cc) for cc in d['creditCars']]
        )
