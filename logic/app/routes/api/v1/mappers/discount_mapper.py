from logic.app.models.discount import Discount
from logic.app.routes.api.v1.mappers import qr_mapper


def discount_to_json(discount: Discount) -> dict:
    j = discount.to_json()

    j['qr'] = qr_mapper.qr_to_json(discount.qr)

    if not discount.discount_price:
        j.pop('discount_price')
    if not discount.discount_percent:
        j.pop('discount_percent')

    return j
