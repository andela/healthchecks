from hc.api.models import Check
from hc.test import BaseTestCase


class CheckManagerTests(BaseTestCase):
    def setUp(self):
        super(CheckManagerTests, self).setUp()
        self.check1 = Check(user=self.alice, name="Alice Was Here")
        self.check1.save()
        self.check2 = Check(user=self.alice, name="Alice was here again")
        self.check2.save()
        self.check3 = Check(user=self.alice, name="Alice never made it here")
        self.check3.status = 'down'
        self.check3.save()

    def test_for_user(self):
        self.assertListEqual(list(Check.objects.for_user(self.alice)), [self.check1, self.check2, self.check3])
        self.assertListEqual(list(Check.objects.for_user(self.alice, True)), [self.check3])
