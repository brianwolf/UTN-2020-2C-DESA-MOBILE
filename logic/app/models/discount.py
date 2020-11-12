from dataclasses import dataclass, field
from typing import List
from uuid import UUID, uuid4

from logic.app.models.qr import Qr


@dataclass
class Discount(object):
    description: str
    qr: Qr
    discount_price: float = None
    discount_percent: float = None
    id: UUID = field(default_factory=uuid4)

    def __eq__(self, other):
        return self.id == other.id

    def to_json(self) -> dict:
        return {
            'description': self.description,
            'qr': self.qr.to_json(),
            'discount_price': self.discount_price,
            'discount_percent': self.discount_percent,
            'id': str(self.id)
        }

    @ staticmethod
    def from_json(d: dict) -> 'Discount':

        id = UUID(str(d.get('id'))) if 'id' in d else uuid4()

        discount_price = float(
            d.get('discount_price')) if d.get('discount_price') else None

        discount_percent = float(
            d.get('discount_percent')) if d.get('discount_percent') else None

        return Discount(
            description=d['description'],
            qr=Qr.from_json(d['qr']),
            discount_price=discount_price,
            discount_percent=discount_percent,
            id=id
        )
