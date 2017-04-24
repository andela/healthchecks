from hc.api.models import Check
from hc.test import BaseTestCase

class PageLinksTestCase(BaseTestCase):

    def test_docs_page(self):
        url = "/docs/"

        r = self.client.get(url)
        assert r.status_code == 200

    def test_about_page(self):
        url = "/about/"
    	
        r = self.client.get(url)
        assert r.status_code == 200

    def test_integrations_page(self):
        url = "/integrations/"
    	
    	# Make sure page is inaccessible not logged in
        r = self.client.get(url)
        assert not r.status_code == 200

        # And is accessible logged in
        self.client.login(username="alice@example.org", password="password")
        r = self.client.get(url)
        assert r.status_code == 200

    def test_checks_page(self):
        url = "/checks/"
    	
        # Make sure page is inaccessible not logged in
        r = self.client.get(url)
        assert not r.status_code == 200

        # And is accessible logged in
        self.client.login(username="alice@example.org", password="password")
        r = self.client.get(url)
        assert r.status_code == 200
