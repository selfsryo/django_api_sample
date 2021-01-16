from api_token.models import Token
from app.tests.factories import factory_user


def factory_token(**kwargs):
    d = {
        'token': 'abcdefghijklmn',
        'user': factory_user()
    }
    d.update(kwargs)
    return Token.objects.create(**d)
