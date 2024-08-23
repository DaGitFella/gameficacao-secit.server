from django.db import models

from api.models import User
from api.models.event import Event
from api.models.stamp import Stamp


class ActivityManager(models.Manager):
    def create(self, **kwargs):
        pass

    def update(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass


class Activity(models.Model):
    stamps_amount = models.IntegerField()
    timestamp = models.DateTimeField()
    type = models.CharField(max_length=128)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    stamp = models.ForeignKey(Stamp, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, blank=True)

    objects = ActivityManager()
