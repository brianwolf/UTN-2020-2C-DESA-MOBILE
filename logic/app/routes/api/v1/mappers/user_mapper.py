from logic.app.models.user import User


def user_to_json(user: User) -> dict:
    j = user.to_json()
    j.get('login').pop('password')
    return j
