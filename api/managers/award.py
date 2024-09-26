from django.db import models


class AwardManager(models.Manager):
    @staticmethod
    def save(awards):
        return AwardManager.bulk_create(awards)

    def update(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass
