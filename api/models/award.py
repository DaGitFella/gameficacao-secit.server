from django.db import models

from api.managers.award import AwardManager
from api.models import User
from api.models.event import Event


class Award(models.Model):
    description = models.CharField(max_length=255)
    required_conquests = models.IntegerField()
    max_quantity = models.IntegerField()
    available_quantity = models.IntegerField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='awards')
    users = models.ManyToManyField(User, blank=True)

    objects = AwardManager()

    def __str__(self):
        return self.description
