from django.db import models

from api.models.conquest import Conquest


class StampManager(models.Manager):
    @staticmethod
    def save(stamps: list):
        for stamp in stamps:
            stamp.save()
        return stamps

    def update(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass
