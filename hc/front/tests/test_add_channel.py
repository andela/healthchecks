from django.test.utils import override_settings

from hc.api.models import Channel
from hc.test import BaseTestCase


@override_settings(PUSHOVER_API_TOKEN="token", PUSHOVER_SUBSCRIPTION_URL="url")
class AddChannelTestCase(BaseTestCase):

    def test_it_adds_email(self):
        url = "/integrations/add/"
        form = {"kind": "email", "value": "alice@example.org"}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, form)

        self.assertRedirects(r, "/integrations/")
        assert Channel.objects.count() == 1

    def test_it_trims_whitespace(self):
        """ Leading and trailing whitespace should get trimmed. """

        url = "/integrations/add/"
        form = {"kind": "email", "value": "   alice@example.org   "}

        self.client.login(username="alice@example.org", password="password")
        self.client.post(url, form)

        q = Channel.objects.filter(value="alice@example.org")
        self.assertEqual(q.count(), 1)

    def test_instructions_work(self):
        self.client.login(username="alice@example.org", password="password")
        kinds = ("email", "webhook", "pd", "pushover", "hipchat", "victorops")
        for frag in kinds:
            url = "/integrations/add_%s/" % frag
            r = self.client.get(url)
            self.assertContains(r, "Integration Settings", status_code=200)

    ### Test that the team access works

    def test_term_access(self):
        url = "/terms/"
        r = self.client.get(url)
        # first make sure its there
        assert r.status_code == 200

        # then see content
        self.assertContains(r, "Terms of Service", status_code=200)

    ### Test that bad kinds don't work

    def test_bad_kinds_dont_work(self):
        self.client.login(username="alice@example.org", password="password")

        # These are not there
        kinds = ("google", "facebook", "uber")

        for kind in kinds:
            url = "/integrations/add_%s/" % kind
            r = self.client.get(url)
            # The integration is not there so a 404 is returned
            assert r.status_code == 404
