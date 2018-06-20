from django.core import mail
from django.utils.timezone import now

from hc.test import BaseTestCase
from hc.accounts.models import Member
from hc.api.models import Check


class ProfileTestCase(BaseTestCase):

    def test_it_sends_set_password_link(self):
        self.client.login(username="alice@example.org", password="password")

        form = {"set_password": "1"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 302

        # profile.token should be set now
        self.alice.profile.refresh_from_db()
        token = self.alice.profile.token
        ### Assert that the token is set

        ### Assert that the email was sent and check email content

    def test_it_sends_report(self):
        check = Check(name="Test Check", user=self.alice)
        check.save()

        self.alice.profile.send_report()

        ###Assert that the email was sent and check email content

    def test_it_adds_team_member(self):
        self.client.login(username="alice@example.org", password="password")

        form = {"invite_team_member": "1", "email": "frank@example.org"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 200

        member_emails = set()
        for member in self.alice.profile.member_set.all():
            member_emails.add(member.user.email)

        ### Assert the existence of the member emails

        self.assertTrue("frank@example.org" in member_emails)

        ###Assert that the email was sent and check email content

    def test_add_team_member_checks_team_access_allowed_flag(self):
        self.client.login(username="charlie@example.org", password="password")

        form = {"invite_team_member": "1", "email": "frank@example.org"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 403

    def test_it_removes_team_member(self):
        self.client.login(username="alice@example.org", password="password")

        form = {"remove_team_member": "1", "email": "bob@example.org"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 200

        self.assertEqual(Member.objects.count(), 0)

        self.bobs_profile.refresh_from_db()
        self.assertEqual(self.bobs_profile.current_team, None)

    def test_it_sets_team_name(self):
        self.client.login(username="alice@example.org", password="password")

        form = {"set_team_name": "1", "team_name": "Alpha Team"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 200

        self.alice.profile.refresh_from_db()
        self.assertEqual(self.alice.profile.team_name, "Alpha Team")

    def test_set_team_name_checks_team_access_allowed_flag(self):
        self.client.login(username="charlie@example.org", password="password")

        form = {"set_team_name": "1", "team_name": "Charlies Team"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 403

    def test_it_switches_to_own_team(self):
        self.client.login(username="bob@example.org", password="password")

        self.client.get("/accounts/profile/")

        # After visiting the profile page, team should be switched back
        # to user's default team.
        self.bobs_profile.refresh_from_db()
        self.assertEqual(self.bobs_profile.current_team, self.bobs_profile)

    def test_it_shows_badges(self):
        self.client.login(username="alice@example.org", password="password")
        Check.objects.create(user=self.alice, tags="foo a-B_1  baz@")
        Check.objects.create(user=self.bob, tags="bobs-tag")

        r = self.client.get("/accounts/profile/")
        self.assertContains(r, "foo.svg")
        self.assertContains(r, "a-B_1.svg")

        # Expect badge URLs only for tags that match \w+
        self.assertNotContains(r, "baz@.svg")

        # Expect only Alice's tags
        self.assertNotContains(r, "bobs-tag.svg")

    def test_it_saves_reports_allowed_true(self):
        self.profile.reports_allowed = False
        self.profile.save()

        self.client.login(username="alice@example.org", password="password")

        form = {"update_reports_allowed":True,"reports_allowed": True, "report_period":"7"}
        r = self.client.post("/accounts/profile/", form)
        self.assertEqual(r.status_code, 200)

        self.profile.refresh_from_db()
        self.assertTrue(self.profile.reports_allowed)
        self.assertIsNotNone(self.profile.next_report_date)

    def test_it_saves_reports_allowed_false(self):
        self.profile.reports_allowed = True
        self.profile.next_report_date = now()
        self.profile.save()

        self.client.login(username="alice@example.org", password="password")

        form = {"update_reports_allowed":True,"reports_allowed": False}
        r = self.client.post("/accounts/profile/", form)
        self.assertEqual(r.status_code, 200)

        self.profile.refresh_from_db()
        self.assertFalse(self.profile.reports_allowed)
        self.assertIsNone(self.profile.next_report_date)

    def test_it_saves_report_period(self):
        self.client.login(username="alice@example.org", password="password")

        form = {"update_reports_allowed":True,"reports_allowed": True,"report_period": "7"}
        r = self.client.post("/accounts/profile/", form)
        self.assertEqual(r.status_code, 200)

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.report_period, 7)
        self.assertIsNotNone(self.profile.next_report_date)
    
    def test_it_does_not_save_non_standard_report_period(self):
        self.profile.report_period = 7
        self.profile.save()

        self.client.login(username="alice@example.org", password="password")

        form = {"update_reports_allowed":True,"reports_allowed": True,"report_period": "17"}
        r = self.client.post("/accounts/profile/", form)
        self.assertEqual(r.status_code, 200)

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.report_period, 7)
