from logic.app.models.cinema import Cinema


def cinema_to_json_short(cinema: Cinema) -> dict:
    j = cinema.to_json()
    j.pop('location')
    j.pop('image_path')
    j.pop('timetables')
    return j
