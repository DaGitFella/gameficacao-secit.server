from django.db import models


class ActivityManager(models.Manager):

    @staticmethod
    def save(activities):
        return ActivityManager.bulk_create(activities)

    def update(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass
