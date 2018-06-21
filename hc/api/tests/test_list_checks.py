import json
from datetime import timedelta as td
from django.utils.timezone import now
from django.http.response import JsonResponse

from hc.api.models import Check
from hc.test import BaseTestCase


class ListChecksTestCase(BaseTestCase):

    def setUp(self):
        super(ListChecksTestCase, self).setUp()

        self.now = now().replace(microsecond=0)

        self.a1 = Check(user=self.alice, name="Alice 1")
        self.a1.timeout = td(seconds=3600)
        self.a1.grace = td(seconds=900)
        self.a1.last_ping = self.now
        self.a1.n_pings = 1
        self.a1.status = "new"
        self.a1.save()

        self.a2 = Check(user=self.alice, name="Alice 2")
        self.a2.timeout = td(seconds=86400)
        self.a2.grace = td(seconds=3600)
        self.a2.last_ping = self.now
        self.a2.status = "up"
        self.a2.save()

    def get(self):
        return self.client.get("/api/v1/checks/", HTTP_X_API_KEY="abc")

    def test_it_works(self):
        r = self.get()
        # Assert the response status code
        self.assertEqual(r.status_code, 200)

        doc = r.json()
        self.assertTrue("checks" in doc)

        checks = {check["name"]: check for check in doc["checks"]}
        # Assert the expected length of checks
        # Expected length of check is two, checks for GET and POST requests only
        length = len(checks)
        self.assertEqual(length, 2)

        # Assert the checks Alice 1 and Alice 2's timeout, grace, ping_url, status,
        name = doc['checks'][0]['name']
        name2 = doc['checks'][1]['name']

        timeout = doc['checks'][0]['timeout']
        timeout2 = doc['checks'][1]['timeout']

        grace = doc['checks'][0]['grace']
        grace2 = doc['checks'][1]['grace']

        ping_url = doc['checks'][0]['ping_url']
        ping_url2 = doc['checks'][1]['ping_url']

        status = doc['checks'][0]['status']
        status2 = doc['checks'][1]['status']

        url = "http://localhost:8000/ping/"

        self.assertEqual(name2, "Alice 1")
        self.assertEqual(timeout, 3600)
        self.assertEqual(grace, 900)
        self.assertEqual(ping_url, url+(str(self.a1.code)))
        self.assertEqual(status, "new")

        self.assertEqual(name, "Alice 2")
        self.assertEqual(timeout2, 86400)
        self.assertEqual(grace2, 3600)
        self.assertEqual(ping_url2, url + str(self.a2.code))
        self.assertEqual(status2, "up")
        # last_ping, n_pings and pause_url

    def test_it_shows_only_users_checks(self):
        bobs_check = Check(user=self.bob, name="Bob 1")
        bobs_check.save()

        r = self.get()
        data = r.json()
        self.assertEqual(len(data["checks"]), 2)
        for check in data["checks"]:
            self.assertNotEqual(check["name"], "Bob 1")

    # Test that it accepts an api_key in the request
    def test_accepts_api_key(self):
        r = self.client.get("/api/v1/checks/", HTTP_X_API_KEY="my_api_key")
        
        # Will accept api and respond with a django JsonResponse object
        self.assertEqual(JsonResponse, type(r))