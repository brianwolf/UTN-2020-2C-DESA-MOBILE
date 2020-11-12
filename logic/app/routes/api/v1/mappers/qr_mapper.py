from logic.app.models.qr import Qr


def qr_to_json(qr: Qr) -> dict:
    j = qr.to_json()
    j.pop('imagen_ruta')
    return j
