from django.contrib.auth.models import User
from django.test import TestCase
from hc.accounts.models import Profile


class TeamAccessMiddlewareTestCase(TestCase):

    def test_it_handles_missing_profile(self):
        total_profiles_before = Profile.objects.count()
        user = User(username="ned", email="ned@example.org")
        user.set_password("password")
        user.save()

        self.client.login(username="ned@example.org", password="password")
        r = self.client.get("/about/")
        self.assertEqual(r.status_code, 200)

        ### Assert the new Profile objects count
        total_profiles_after = Profile.objects.count()
        self.assertEqual(total_profiles_after, total_profiles_before + 1)
