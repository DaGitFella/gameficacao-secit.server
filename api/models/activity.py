from django.db import models

from api.managers.activity import ActivityManager
from api.models import User
from api.models.event import Event
from api.models.stamp import Stamp


class Activity(models.Model):
    stamps_amount = models.IntegerField()
    type = models.CharField(max_length=128)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='activities')
    stamp = models.ForeignKey(Stamp, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, blank=True, through='api.UserActivity')

    objects = ActivityManager()

    def __str__(self):
        return f'{self.type} | {self.stamps_amount}'
