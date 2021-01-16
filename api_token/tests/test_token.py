import json

from django.test import TestCase, RequestFactory
from django.urls import reverse

from app.models import Combi
from app.tests.factories import (
    factory_user,
    factory_office,
    factory_combi,
)
from api_token.tests.factories import factory_token


TOKEN_CREATE_URL = reverse('api_token:create')
COMBI_CREATE_URL = reverse('app:create')


class TestCreateAPIToken(TestCase):

    def setUp(self):
        self.user = factory_user(
            username='テストユーザー',
            email='test@example.com'
        )

    def test_create_api_token_success(self):
        """トークン作成成功"""
        self.client.force_login(self.user)
        res = self.client.get(TOKEN_CREATE_URL)

        self.assertEqual(res.status_code, 201)

        msg = json.loads(res.content)['message']
        self.assertEqual(msg, 'トークンを作成しました')

    def test_not_login(self):
        """未ログインでトークン作成"""
        res = self.client.get(TOKEN_CREATE_URL)

        self.assertEqual(res.status_code, 403)

        msg = json.loads(res.content)['message']
        self.assertEqual(msg, 'ログインしてください')

    def test_already_has_token(self):
        """素手にトークンを持った状態で作成"""
        self.client.force_login(self.user)
        token = factory_token(user=self.user)

        res = self.client.get(TOKEN_CREATE_URL)
        self.assertEqual(res.status_code, 200)

        msg = json.loads(res.content)['message']
        self.assertEqual(msg, '既にトークンがあります')

        token = json.loads(res.content)['token']
        self.assertEqual(token, self.user.token.token)


class TestCreateCombiWithToken(TestCase):

    def setUp(self):
        self.user = factory_user(
            username='テストユーザー',
            email='test@example.com'
        )
        self.client.force_login(self.user)

    def test_not_create_token(self):
        """トークン未取得でコンビ作成"""
        res = self.client.post(COMBI_CREATE_URL, json.dumps({
            'name': 'NON STYLE',
            'office': '吉本興業',
        }), content_type='application/json')

        self.assertEqual(res.status_code, 400)

        msg = json.loads(res.content)['message']
        self.assertEqual(msg, 'トークンを取得してください')
        self.assertEqual(Combi.objects.count(), 0)

    def test_not_set_token(self):
        """トークンをヘッダに含まずにコンビ作成"""
        factory_token(user=self.user)
        res = self.client.post(COMBI_CREATE_URL, json.dumps({
            'name': 'サンドウィッチマン',
            'office': 'グレープカンパニー',
        }), content_type='application/json')

        self.assertEqual(res.status_code, 401)

        msg = json.loads(res.content)['message']
        self.assertEqual(msg, 'リクエストヘッダにトークンが含まれていません')
        self.assertEqual(Combi.objects.count(), 0)

    def test_invalid_token(self):
        """他のユーザーのトークンでコンビ作成"""
        request1 = RequestFactory()
        request1.user = self.user
        factory_token(request=request1)

        request2 = RequestFactory()
        request2.user = factory_user()
        token2 = factory_token(request=request2)

        self.header = {'HTTP_AUTHORIZATION': 'Token ' + token2.token}

        res = self.client.post(COMBI_CREATE_URL, json.dumps({
            'name': 'チュートリアル',
            'office': '吉本興業',
        }), content_type='application/json', **self.header)
        self.assertEqual(res.status_code, 400)

        msg = json.loads(res.content)['message']
        self.assertEqual(msg, 'トークンが異なります')
        self.assertEqual(Combi.objects.count(), 0)

    def test_not_set_auth_type(self):
        """認証タイプを含めずコンビ作成"""
        token = factory_token(user=self.user)
        header = {'HTTP_AUTHORIZATION': token.token}
        res = self.client.post(COMBI_CREATE_URL, json.dumps({
            'name': 'ブラックマヨネーズ',
            'office': '吉本興業',
        }), content_type='application/json', **header)

        self.assertEqual(res.status_code, 400)

        msg = json.loads(res.content)['message']
        self.assertEqual(msg, 'トークンが異なります')
        self.assertEqual(Combi.objects.count(), 0)


class TestDeleteCombiWithToken(TestCase):

    def setUp(self):
        self.user = factory_user(
            username='ユーザー1',
            email='test@example.com'
        )
        self.client.force_login(self.user)

        office = factory_office(name='人力舎')
        self.combi = factory_combi(name='アンタッチャブル', office=office)
        self.url = reverse('app:delete', args=[self.combi.pk])

    def test_not_create_token(self):
        """トークン未取得でコンビ削除"""
        res = self.client.delete(self.url)

        self.assertEqual(res.status_code, 400)

        msg = json.loads(res.content)['message']
        self.assertEqual(msg, 'トークンを取得してください')
        self.assertEqual(Combi.objects.count(), 1)

    def test_not_set_token(self):
        """トークンをヘッダに含まずにコンビ削除"""
        factory_token(user=self.user)
        res = self.client.delete(self.url)

        self.assertEqual(res.status_code, 401)

        msg = json.loads(res.content)['message']
        self.assertEqual(msg, 'リクエストヘッダにトークンが含まれていません')
        self.assertEqual(Combi.objects.count(), 1)

    def test_invalid_token(self):
        """他のユーザーのトークンでコンビ削除"""
        request1 = RequestFactory()
        request1.user = self.user
        factory_token(request=request1)

        request2 = RequestFactory()
        request2.user = factory_user()
        tk = factory_token(request=request2)

        self.header = {'HTTP_AUTHORIZATION': 'Token ' + tk.token}

        res = self.client.delete(self.url, **self.header)
        self.assertEqual(res.status_code, 400)

        msg = json.loads(res.content)['message']
        self.assertEqual(msg, 'トークンが異なります')
        self.assertEqual(Combi.objects.count(), 1)

    def test_not_set_auth_type(self):
        """認証タイプを含めずコンビ削除"""
        token = factory_token(user=self.user)
        header = {'HTTP_AUTHORIZATION': token.token}
        res = self.client.delete(self.url, **header)

        self.assertEqual(res.status_code, 400)

        msg = json.loads(res.content)['message']
        self.assertEqual(msg, 'トークンが異なります')
        self.assertEqual(Combi.objects.count(), 1)
