import random

from api_token.models import Token
from api_token.authentication import create_token
from app.tests.factories import factory_user


def factory_token(**kwargs):
    if 'request' in kwargs:
        return create_token(kwargs['request'])
    else:
        d = {
            'token': ''.join(
                random.choice('abcdefghijklmn') for _ in range(100)
            ),
            'user': factory_user()
        }
        d.update(kwargs)
        return Token.objects.create(**d)
