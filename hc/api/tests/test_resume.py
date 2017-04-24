from hc.api.models import Check
from hc.test import BaseTestCase

class ResumeTestCase(BaseTestCase):   

    def test_it_works(self):
        check = Check(user=self.alice, status="paused")
        check.save()

        r = self.client.get("/ping/%s/" % check.code)
        assert r.status_code == 200

        check.refresh_from_db()
        assert check.status == "up"
