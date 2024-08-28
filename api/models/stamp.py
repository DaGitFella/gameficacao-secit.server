from django.db import models

from api.models.conquest import Conquest
from api.models.event import Event


class StampManager(models.Manager):
    def create(self, **kwargs):
        stamp = self.model(**kwargs)
        stamp.save()
        return stamp

    def update(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass


class Stamp(models.Model):
    icon = models.CharField(max_length=128)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='stamps')
    conquest = models.ForeignKey(Conquest, on_delete=models.CASCADE)

    objects = StampManager()

    def __str__(self):
        return self.icon
