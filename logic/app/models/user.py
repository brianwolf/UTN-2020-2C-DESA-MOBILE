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
        return self.__dict__.copy()

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
        return self.__dict__.copy()

    @staticmethod
    def from_json(d: dict) -> 'CreditCard':
        return CreditCard(**d)


@dataclass
class DiscountUser(object):
    id: UUID = uuid4()
    date_scanned: datetime = datetime.now()

    def __eq__(self, other):
        return self.id == other.id

    def to_json(self) -> dict:
        return self.__dict__.copy()

    @staticmethod
    def from_json(d: dict) -> 'DiscountUser':
        id = UUID(str(d.get('id'))) if 'id' in d else uuid4()

        date_scanned = datetime.fromisoformat(
            d.get('date_scanned')) if 'date_scanned' in d else datetime.now()

        return User(
            id=id,
            date_scanned=date_scanned
        )


@dataclass
class User(object):
    login: Login
    creditCars: List[CreditCard] = field(default_factory=list)
    last_conection: datetime = datetime.now()
    discounts: List[DiscountUser] = field(default_factory=list)
    id: UUID = uuid4()

    def __eq__(self, other):
        return self.id == other.id

    def to_json(self) -> dict:
        return {
            'id': str(self.id),
            'last_conection': self.last_conection.isoformat(),
            'creditCars': [o.to_json() for o in self.creditCars],
            'discounts': [o.to_json() for o in self.discounts],
            'login': self.login.to_json()
        }

    @staticmethod
    def from_json(d: dict) -> 'Qr':

        id = UUID(str(d.get('id'))) if 'id' in d else uuid4()

        last_conection = datetime.fromisoformat(
            d.get('last_conection')) if 'last_conection' in d else datetime.now()

        return User(
            login=Login.from_json(d.get('login', {})),
            id=id,
            last_conection=last_conection,
            creditCars=[CreditCard.from_json(j)
                        for j in d.get('creditCars', [])],
            discounts=[DiscountUser.from_json(j)
                       for j in d.get('discounts', [])]
        )
