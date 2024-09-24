from django.db import models

from api.managers.stamp import StampManager
from api.models.conquest import Conquest


class Stamp(models.Model):
    icon = models.CharField(max_length=128)
    conquest = models.ForeignKey(Conquest, on_delete=models.CASCADE, related_name='stamps')

    objects = StampManager()

    def __str__(self):
        return self.icon
