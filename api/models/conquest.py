from django.db import models

from api.models.event import Event


class ConquestManager(models.Manager):
    def create(self, **kwargs):
        pass

    def update(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass


class Conquest(models.Model):
    name = models.CharField(max_length=255, unique=True)
    color = models.CharField(max_length=255)
    required_stamps = models.IntegerField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    objects = ConquestManager()
