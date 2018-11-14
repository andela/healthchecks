from hc.api.models import Check
from hc.test import BaseTestCase


class AddCheckTestCase(BaseTestCase):

    def test_it_works(self):
        url = "/checks/add/"
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)
        self.assertRedirects(r, "/checks/")
        assert Check.objects.count() == 1

    ### Test that team access works

    def test_term_access(self):
        url = "/terms/"
        r = self.client.get(url)
        # first make sure its there
        assert r.status_code == 200
        # then check content
        self.assertContains(r, "Terms of Service", status_code=200)

