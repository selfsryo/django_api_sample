import random

from django.contrib.auth import get_user_model

from app.models import Office, Combi


def factory_user(**kwargs):
    d = {
        'username': ''.join(random.choice('abcdef') for _ in range(10)),
        'email': 'test@example.com',
        'password': 'secure123'
    }
    d.update(kwargs)
    return get_user_model().objects.create(**d)


def factory_office(**kwargs):
    d = {
        'name': 'テストオフィス',
    }
    d.update(kwargs)
    return Office.objects.create(**d)


def factory_combi(**kwargs):
    d = {
        'name': 'テストコンビ',
        'office': factory_office()
    }
    d.update(kwargs)
    return Combi.objects.create(**d)
