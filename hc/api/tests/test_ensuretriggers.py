from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from hc.api.management.commands.ensuretriggers import Command
from hc.api.models import Check


class EnsureTriggersTestCase(TestCase):

    def test_ensure_triggers(self):
        Command().handle()

        check = Check.objects.create()
        self.assertEquals(check.alert_after, None) #

        check.last_ping = timezone.now()
        check.save()
        check.refresh_from_db()
        # if trigger passes, the alert_after field in database should have a value of same type  the timezone.now() value
        self.assertIsInstance(check.alert_after, type(timezone.now()))         

        my_alert_after = check.alert_after

        check.last_ping += timedelta(days=1)
        check.save()
        check.refresh_from_db()

        ### Assert that alert_after is lesser than the check's alert_after
        self.assertLess(my_alert_after, check.alert_after)
        
