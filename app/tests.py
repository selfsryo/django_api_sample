import json
from django.test import TestCase
from app.models import Combi


class TestViews(TestCase):

    def test_api_combi(self):
        # 正常、タグつき
        res = self.client.post("/api/combi/create", json.dumps({
            "name": "霜降り明星",
            "office": "吉本興業",
        }), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(Combi.objects.count(), 1)
