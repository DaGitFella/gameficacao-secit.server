from django.db import models


class ActivityManager(models.Manager):

    def save(self, activities):
        return self.bulk_create(activities)

    def update(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass
