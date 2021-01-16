import json

from django.test import TestCase
from django.urls import reverse

from app.tests.factories import (
    factory_user,
    factory_office,
    factory_combi,
)
from api_token.tests.factories import factory_token


TOKEN_CREATE_URL = reverse('api_token:create')


class TestCreateAPIToken(TestCase):

    def setUp(self):
        self.user = factory_user(
            username='ユーザー1', 
            email='test@example.com'
        )

    def test_create_api_token_success(self):
        self.client.force_login(self.user)
        res = self.client.get(TOKEN_CREATE_URL)

        self.assertEqual(res.status_code, 201)

        msg = json.loads(res.content)['message']
        self.assertEqual(msg, 'トークンを作成しました')

    def test_not_login(self):
        res = self.client.get(TOKEN_CREATE_URL)

        self.assertEqual(res.status_code, 403)

        msg = json.loads(res.content)['message']
        self.assertEqual(msg, 'ログインしてください')

    def test_already_has_token(self):
        self.client.force_login(self.user)
        token = factory_token(user=self.user)

        res = self.client.get(TOKEN_CREATE_URL)
        self.assertEqual(res.status_code, 200)

        msg = json.loads(res.content)['message']
        self.assertEqual(msg, '既にトークンがあります')

        token = json.loads(res.content)['token']
        self.assertEqual(token, self.user.token.token)

