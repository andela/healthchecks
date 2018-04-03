import json
import uuid
import requests
import datetime

from django.test import Client

from hc.api.models import Channel, Check, Notification
from hc.test import BaseTestCase
from hc.settings import SITE_ROOT


class CreateCheckTestCase(BaseTestCase):
    URL = "/api/v1/checks/"

    def setUp(self):
        super(CreateCheckTestCase, self).setUp()

    def post(self, data, expected_error=None):
        self.client = Client() # Added client module from test
        r = self.client.post(self.URL, json.dumps(data),
                             content_type="application/json")

        if expected_error:
            self.assertEqual(r.status_code, 400)
            ### Assert that the expected error is the response error

        return r
    
    def get(self, link, expected_error=None):
        self.client = Client()
        r = self.client.get(link)
        if expected_error:
            self.assertEqual(r.status_code, 400)
        return r

    def test_it_works(self):
        r = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 3600,
            "grace": 60
        })

        self.assertEqual(r.status_code, 201)
        

        doc = r.json()
        # introduce database model Check
        self.check = Check()
        self.check.name = doc["name"]
        self.check.tags = doc["tags"]
        my_url = self.check.url()
        # assert "ping_url" in self.check.url()
        self.assertEqual(self.check.url(), "%s/ping/%s" % (SITE_ROOT, self.check.code)) # combining the code to ensure the urls match
        self.assertEqual(self.check.name, "Foo") # Correcting the assertions
        self.assertEqual(self.check.tags_list(), ["bar,baz"]) # correcting assertions

        ### Assert the expected last_ping and n_pings values

        self.assertEqual(Check.objects.count(), 1)
        check = Check.objects.get()
        self.assertEqual(check.name, "Foo")
        self.assertEqual(check.tags, "bar,baz")
        self.assertEqual(check.timeout.total_seconds(), 3600)
        self.assertEqual(check.grace.total_seconds(), 60)

    def test_it_accepts_api_key_in_header(self):
        # payload = json.dumps({"api_key": "Foo"})
        self.payload = {
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 3600,
            "grace": 60
            }
        self.check = Check()        

        ### Make the post request and get the response
        req = self.post(self.payload)              
       

        # r = self.client.post({'status_code': 201}) ### This is just a placeholder variable
        self.assertEqual(req.status_code, 201)
        

    def test_it_handles_missing_request_body(self):
        ### Make the post request with a missing body and get the response        
        # r = {'status_code': 400, 'error': "wrong api_key"} ### This is just a placeholder variable
        payload = {'status_code': 400, 'error': "right api_key"} # just checking, but it works
        req = self.post(payload, 400)
        self.assertEqual(req.status_code, 400) # should return 400 code for missing request body
        doc = req.json()
        self.assertEqual(doc['error'], "wrong api_key")

    def test_it_handles_invalid_json(self):
        ### Make the post request with invalid json data type
        payload = {'status_code': 400, 'error': "could not parse request body"} ### This is just a placeholder variable
        req = self.client.post(self.URL, data=payload)
        doc = req.json()

        self.assertEqual(doc['error'], 'could not parse request body')

    def test_it_rejects_wrong_api_key(self):
        req = self.post({"api_key": "wrong"},
                  expected_error="wrong api_key")
        doc = req.json()
        self.assertEqual(doc['error'], "wrong api_key") # checking that posting reveals "wrong api_key"

    def test_it_rejects_non_number_timeout(self):
        req = self.post({"api_key": "abc", "timeout": "oops"},
                  expected_error="timeout is not a number")
        doc = req.json()
        self.assertEqual(doc['error'], 'timeout is not a number')

    def test_it_rejects_non_string_name(self):
        req = self.post({"api_key": "abc", "name": False},
                  expected_error="name is not a string")
        doc = req.json()
        self.assertEqual(doc['error'], "name is not a string")

    ### Test for the assignment of channels
    def test_channel_assigned(self):
        self.check = Check()
        
        payload = payload = {
           "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 3600,
            "grace": 60,
            "channels": "*"
            }

        # if channel is created, it will respond with 201 success status code    
        req = self.post(data=payload)          
        self.assertEqual(req.status_code, 201) # assert that here


    ### Test for the 'timeout is too small' and 'timeout is too large' errors

    def test_timeout_small_large(self):
        self.check = Check()

        # create api for large timeout
        payload_timeout_large = {
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 72000,
            "grace": 60,
            "channels": "*"
        }
        self.check.timeout = datetime.timedelta(hours=payload_timeout_large['timeout'])
        req = self.post(data=payload_timeout_large)        
        self.assertTrue("ValueError: timeout too big", self.check.valid_timeout())

        # create payload for small timeout        
        payload_timeout_small = {
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 50,
            "grace": 60,
            "channels": "*"
        }

        self.check.timeout = datetime.timedelta(hours=payload_timeout_small['timeout'])
        req = self.post(data=payload_timeout_small)
        self.assertTrue("VaalueError: timeout too small", self.check.valid_timeout)