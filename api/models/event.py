from django.db import models

from api.managers.event import EventManager
from api.models import User


class Event(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField()
    edition_number = models.IntegerField()
    user_who_created = models.ForeignKey(User, related_name='events_created', on_delete=models.CASCADE)
    users_who_participate = models.ManyToManyField(User, related_name='events_participating')

    objects = EventManager()
