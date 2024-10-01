from django.db import models

from api.managers.conquest import ConquestManager
from api.models.event import Event


class Conquest(models.Model):
    name = models.CharField(max_length=255, unique=True)
    color = models.CharField(max_length=6)
    required_stamps = models.IntegerField()
    min_stamp_types_amount = models.IntegerField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='conquests')

    objects = ConquestManager()

    def __str__(self):
        return f'{self.name} | {self.id}'
