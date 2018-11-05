from datetime import timedelta, datetime

from django.test import TestCase, Client
from django.utils import timezone
from hc.api.models import Check, Notification, DEFAULT_TIMEOUT, DEFAULT_GRACE


class CheckModelTestCase(TestCase):    
         
    def test_it_strips_tags(self):
        check = Check()

        check = Check()
        check.last_ping = timezone.now() 
        check.timeout = timezone.timedelta(days=1) # 
        check.grace = timezone.timedelta(hours=1)          
        
        up_ends = check.last_ping + check.timeout
        grace_ends = up_ends + check.grace  

        check.tags = " foo  bar "
        self.assertEquals(check.tags_list(), ["foo", "bar"])
        ### Repeat above test for when check is an empty string
        check.tags = ""
        self.assertEquals(check.tags_list(), [])

    def test_status_works_with_grace_period(self):
        check = Check()
        check.last_ping = timezone.now() 
        check.timeout = timezone.timedelta(days=1) # 
        check.grace = timezone.timedelta(hours=1)          
        
        up_ends = check.last_ping + check.timeout
        grace_ends = up_ends + check.grace  
        
        self.assertEqual(check.in_grace_period(), up_ends < check.last_ping < grace_ends)
        self.assertEqual(check.get_status(), check.status)

        


        ### The above 2 asserts fail. Make them pass

    def test_paused_check_is_not_in_grace_period(self):
        check = Check()      

        my_status = ["up", "paused"]
        for stat in my_status:
            if stat == "up":
                check.status = stat
                check.last_ping = timezone.now()
                check.timeout = timezone.timedelta(days=1)
                check.grace_period = timezone.timedelta(hours=1)

                up_ends = check.last_ping + check.timeout
                grace_ends = up_ends + check.grace

                self.assertEqual(check.get_status(), "up")
                self.assertEqual(check.in_grace_period(), up_ends < check.last_ping < grace_ends)
            else:
                check.status = stat
                check.last_ping = timezone.now()
                check.timeout = timezone.timedelta(days=1)
                check.grace_period = timezone.timedelta(hours=1)

                up_ends = check.last_ping + check.timeout
                grace_ends = up_ends + check.grace

                self.assertEqual(check.get_status(), "paused")
                self.assertEqual(check.in_grace_period(), up_ends < check.last_ping < grace_ends)


    ### Test that when a new check is created, it is not in the grace period
    def test_new_check_not_in_grace_period(self):
        check = Check()
        check.last_ping = timezone.now()
        check.grace_period = timezone.timedelta(hours=1)     
        self.assertFalse(check.in_grace_period(), False) # less than the grace period and not enough time for up status
