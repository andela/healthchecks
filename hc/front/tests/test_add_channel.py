"""Tesing moddule for channels"""

from django.test.utils import override_settings
from django.test import Client

from hc.api.models import Channel, Check, CHANNEL_KINDS
from hc.accounts.models import Profile, Member
from hc.settings import PING_ENDPOINT
from hc.test import BaseTestCase


@override_settings(PUSHOVER_API_TOKEN="token", PUSHOVER_SUBSCRIPTION_URL="url")

class AddChannelTestCase(BaseTestCase):
    """Tests for Adding Channel"""

    def test_it_adds_email(self):
        """Tests to see if email is added"""

        url = "/integrations/add/"
        form = {"kind" : "email", "value" : "alice@example.org"}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, form)

        self.assertRedirects(r, "/integrations/")        
        self.assertEquals(Channel.objects.count(), 1) # corrected the assertEquals()  method

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
# class ChangeTeamTestCase(BaseTestCase):
#     """Testing team access works"""

#     def set_up(self):
#         self.client = Client()       
        
#     def test_switch_team_works(self):
#         """Test Switch team works"""
#         response = self.client.get('switch_team/([\w-]+)')
#         self.assertEqual(response.status_code, 404)
        
            
# ### Test that bad kinds don't work

class KindsTestCase(BaseTestCase):
    """Testing that only supported kinds work"""
    def test_that_unsupported_kinds_dont_work(self):
        """check to ensure exception message raises"""
        self.kind = "not_exists"
        my_channel = Channel()
        my_channel.kind = self.kind
        self.assertRaisesMessage(NotImplementedError, "NotImplementedError: Unknown channel kind: not_exits")
       


    
    
