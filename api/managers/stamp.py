from django.db import models

from api.models.conquest import Conquest


class StampManager(models.Manager):
    @staticmethod
    def save(stamps):
        return StampManager.bulk_create(stamps)

    def update(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass
