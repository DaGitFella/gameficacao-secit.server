from django.db import models

from api.models.event import Event


class ConquestManager(models.Manager):
    def create(self, **kwargs):
        conquest = self.model(**kwargs)
        conquest.save()
        return conquest

    def update(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass


class Conquest(models.Model):
    name = models.CharField(max_length=255, unique=True)
    color = models.CharField(max_length=255)
    required_stamps = models.IntegerField()
    min_stamp_types_amount = models.IntegerField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='conquests')

    objects = ConquestManager()

    def __str__(self):
        return self.name
