from datetime import timedelta
import time

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone
from hc.accounts.models import Profile
from hc.api.models import Check


def num_pinged_checks(profile):
    q = Check.objects.filter(user_id=profile.user.id,)
    q = q.filter(last_ping__isnull=False)
    return q.count()


class Command(BaseCommand):
    help = 'Send due monthly reports'
    tmpl = "Sending monthly report to %s"

    def add_arguments(self, parser):
        parser.add_argument(
            '--loop',
            action='store_true',
            dest='loop',
            default=False,
            help='Keep running indefinitely in a 300 second wait loop',
        )

    def handle_one_run(self):
        now = timezone.now()

        report_due = Q(next_report_date__lt=now)
        report_not_scheduled = Q(next_report_date__isnull=True)

        q = Profile.objects.filter(report_due | report_not_scheduled)
        q = q.filter(reports_allowed=True)
        profile = q.first()

        if profile is None:
            return False
        
        report_start_date = now - timedelta(days=profile.report_period)
        report_end_date = now + timedelta(days=profile.report_period)
        
        if profile.user.date_joined > report_start_date:
            return False
        
        # Try to update next_report_date
        current_profile = Profile.objects.filter(id=profile.id, next_report_date=profile.next_report_date)

        num_updated = current_profile.update(next_report_date=report_end_date)
        if num_updated != 1:
            # next_report_date was already updated elsewhere, skipping
            return True

        if profile.send_report():
            self.stdout.write(self.tmpl % profile.user.email)
            # Pause before next report to avoid hitting sending quota
            self.pause()

        return True

    def handle(self, *args, **options):
        self.stdout.write("sendreports is now running")
        while True:
            while self.handle_one_run():
                pass

            if not options["loop"]:
                break

            formatted = timezone.now().isoformat()
            self.stdout.write("-- MARK %s --" % formatted)

            time.sleep(300)
