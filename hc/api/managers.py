from django.db import models


class CheckManager(models.Manager):
    def for_user(self, user, failed_only=None):
        if failed_only:
            return self.filter(user=user, status='down')
        return self.filter(user=user).order_by('created')
