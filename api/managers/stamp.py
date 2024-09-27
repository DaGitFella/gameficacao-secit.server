from django.db import models

from api.models.conquest import Conquest


class StampManager(models.Manager):
    def save(self, stamps: list):
        return self.bulk_create(stamps)

    def update(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass
