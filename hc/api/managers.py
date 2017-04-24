from django.db import models


class CheckManager(models.Manager):
    def for_user(self, user, failed_only=None):
        """
        Check for specific user

        :param user: The user whose check are queried (models.User)
        :param failed_only: Whether to return only those that failed or not (Boolean)
        :return: Queryset (self.model)
        """
        if failed_only:
            return self.for_user(user).filter(status='down')
        return self.filter(user=user).order_by('created')