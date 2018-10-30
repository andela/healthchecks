from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from hc.api.models import Check


class LoginTestCase(TestCase):

    def test_it_sends_link(self):
        check = Check()
        check.save()

        session = self.client.session
        session["welcome_code"] = str(check.code)
        session.save()

        form = {"email": "alice@example.org"}

        r = self.client.post("/accounts/login/", form)
        assert r.status_code == 302

        ### Assert that a user was created
        self.assertEqual(User.objects.count(), 1)
        # And email sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Log in to healthchecks.io')
        ### Assert contents of the email body
        self.assertIn('Need help getting started? Check',mail.outbox[0].body)

        ### Assert that check is associated with the new user
        check_again = Check.objects.get(code=check.code)
        assert check_again.user

    def test_it_pops_bad_link_from_session(self):
        self.client.session["bad_link"] = True
        self.client.get("/accounts/login/")
        assert "bad_link" not in self.client.session

        ### Any other tests?
    def test_it_handles_password(self):
        alice = User(username="alice", email="alice@example.org")
        alice.set_password("password")
        alice.save()

        form = {
            "action": "login",
            "email": "alice@example.org",
            "password": "password"
        }

        r = self.client.post("/accounts/login/", form)
        self.assertEqual(r.status_code, 302)
    def test_it_handles_wrong_password(self):
        alice = User(username="alice", email="alice@example.org")
        alice.set_password("password")
        alice.save()

        form = {
            "action": "login",
            "email": "alice@example.org",
            "password": "wrong password"
        }

        r = self.client.post("/accounts/login/", form)
        self.assertContains(r, "Incorrect email or password")
