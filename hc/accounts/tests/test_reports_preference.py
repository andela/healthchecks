from datetime import timedelta

from hc.test import BaseTestCase
from hc.accounts.models import Member
from hc.api.models import Check

from django.utils import timezone

class ReportsPreferenceTestCase(BaseTestCase):

	def test_it_updates_option(self):
		#checks if the form actally works and there are no errors
		self.client.login(username="alice@example.org", password="password")
		form = {"update_reports_allowed": "1", "reports_allowed": "weekly"}

		r = self.client.post("/accounts/profile/", form)
		self.assertEquals(r.status_code, 200)

	def test_new_option_is_correct(self):
		#checks if the value in db is same as what was passed 
		self.client.login(username="alice@example.org", password="password")
		form = {"update_reports_allowed": "1", "reports_allowed": "daily"}

		r = self.client.post("/accounts/profile/", form)

		self.alice.profile.refresh_from_db()
		self.assertEquals(self.alice.profile.reports_allowed, "daily")

	def test_next_report_date_correct(self):
		#Checks if the next report date is set correctly. For weekly,
		#the next date should be 7 days from now
		check = Check(name="Test Check", user=self.alice)
		check.save()

		time_now = timezone.now()

		self.alice.profile.reports_allowed = 'weekly'
		self.alice.profile.save()
		self.alice.profile.send_report()
		self.alice.profile.refresh_from_db()

		days_from_now = self.alice.profile.next_report_date - time_now

		self.assertEquals(days_from_now.days, 7)