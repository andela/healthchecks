from django.contrib.auth.hashers import make_password
from hc.test import BaseTestCase


class CheckTokenTestCase(BaseTestCase):

    def setUp(self):
        super(CheckTokenTestCase, self).setUp()
        self.profile.token = make_password("secret-token")
        self.profile.save()

    def test_it_shows_form(self):
        r = self.client.get("/accounts/check_token/alice/secret-token/")
        self.assertContains(r, "You are about to log in")

    def test_it_redirects(self):
        r = self.client.post("/accounts/check_token/alice/secret-token/")
        self.assertRedirects(r, "/checks/")

        # After login, token should be blank
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.token, "")

    ### Login and test it redirects already logged in
    def test_redirect_after_login(self):
        # login
        self.client.login(username="alice@example.org", password="password")

        #after being authenticated, login again and check for redirection
        login_request = self.client.post("/accounts/check_token/alice/secret-token/")
        self.assertRedirects(login_request, "/checks/")

    ### Login with a bad token and check that it redirects
    def test_redirect_bad_token_login(self):
        bad_login_request = self.client.post("/accounts/check_token/alice/bad_token/")
        self.assertRedirects(bad_login_request,"/accounts/login/")

    ### Any other tests?
    def test_check_ready_to_login(self):
        response = self.client.get("/accounts/check_token/alice/random_token/")
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'accounts/check_token_submit.html')
        self.assertContains(response, 'You are about to log into healthchecks.io.')
