import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from app.models import Combi
from app.tests.factories import (
    factory_user,
    factory_office,
    factory_combi,
)
from api_token.tests.factories import factory_token


COMBI_CREATE_URL = reverse('app:create')
COMBI_LIST_URL = reverse('app:list')


class TestCreateAPICombi(TestCase):

    def setUp(self):
        self.token = factory_token()
        self.user = self.token.user
        self.client.force_login(self.user)
        self.header = {'HTTP_AUTHORIZATION': self.token.token}

    def test_create_combi_success(self):
        res = self.client.post(COMBI_CREATE_URL, json.dumps({
            'name': 'マヂカルラブリー',
            'office': '吉本興業',
        }), content_type='application/json', **self.header)

        self.assertEqual(res.status_code, 201)

        msg = json.loads(res.content)['message']
        self.assertEqual(msg, 'マヂカルラブリーを作成しました')
        self.assertEqual(Combi.objects.count(), 1)

    def test_create_combi_fail(self):
        res = self.client.post(COMBI_CREATE_URL, json.dumps({
            'name': 'ミルクボーイ',
        }), content_type='application/json', **self.header)

        self.assertEqual(res.status_code, 400)

        msg = json.loads(res.content)['message']
        self.assertEqual(msg, 'officeを含めてください')
        self.assertEqual(Combi.objects.count(), 0)

        res = self.client.post(COMBI_CREATE_URL, json.dumps({
            'office': '吉本興業',
        }), content_type='application/json', **self.header)
        self.assertEqual(res.status_code, 400)

        msg = json.loads(res.content)['message']
        self.assertEqual(msg['name'], ['このフィールドは必須です。'])
        self.assertEqual(Combi.objects.count(), 0)

    def test_invalid_method(self):
        res = self.client.get(COMBI_CREATE_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.content), {})


class TestListAPICombi(TestCase):

    def setUp(self):
        self.user = factory_user()
        self.client.force_login(self.user)

        office = factory_office(name='吉本興業')
        combi1 = factory_combi(name='霜降り明星', office=office)
        combi2 = factory_combi(name='とろサーモン', office=office)
        combi3 = factory_combi(name='銀シャリ', office=office)

    def test_get_combi_list(self):
        res = self.client.get(COMBI_LIST_URL)

        self.assertEqual(res.status_code, 200)

        combi_dict = json.loads(res.content)
        self.assertEqual(len(combi_dict), 3)
        self.assertEqual(combi_dict[0]['name'], '霜降り明星')


class TestDetailAPICombi(TestCase):

    def setUp(self):
        self.user = factory_user()
        self.client.force_login(self.user)

        office = factory_office(name='吉本興業')
        self.combi1 = factory_combi(name='トレンディエンジェル', office=office)
        self.combi2 = factory_combi(name='笑い飯', office=office)

    def test_get_combi_detail(self):
        url1 = reverse('app:detail', args=[self.combi1.pk])
        res = self.client.get(url1)
        self.assertEqual(res.status_code, 200)

        combi_dict = json.loads(res.content)
        self.assertEqual(combi_dict['name'], 'トレンディエンジェル')

        url2 = reverse('app:detail', args=[self.combi2.pk])
        res = self.client.get(url2)

        combi_dict = json.loads(res.content)
        self.assertEqual(combi_dict['name'], '笑い飯')

    def test_not_exist_combi(self):
        url = reverse('app:detail', args=[3])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 404)

        msg = json.loads(res.content)['message']
        self.assertEqual(msg, '存在しないコンビです')


class TestDeleteAPICombi(TestCase):

    def setUp(self):
        self.token = factory_token()
        self.user = self.token.user
        self.client.force_login(self.user)
        self.header = {'HTTP_AUTHORIZATION': self.token.token}

        office = factory_office(name='吉本興業')
        self.combi = factory_combi(name='パンクブーブー', office=office)

    def test_delete_combi_success(self):
        url = reverse('app:delete', args=[self.combi.pk])
        res = self.client.delete(url, **self.header)

        msg = json.loads(res.content)['message']
        self.assertEqual(msg, 'パンクブーブーを削除しました')

    def test_not_exist_combi(self):
        url = reverse('app:delete', args=[2])
        res = self.client.delete(url, **self.header)

        self.assertEqual(res.status_code, 404)

        msg = json.loads(res.content)['message']
        self.assertEqual(msg, '存在しないコンビです')

    def test_invalid_method(self):
        url = reverse('app:delete', args=[self.combi.pk])
        res = self.client.get(url, **self.header)

        self.assertEqual(res.status_code, 405)
        msg = json.loads(res.content)['message']
        self.assertEqual(msg, 'DELETEメソッドのみ受け付けます')
