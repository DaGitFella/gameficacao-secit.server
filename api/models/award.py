from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

from api.models.conquest import Conquest
from api.models.event import Event


class AwardManager(models.Manager):
    def create(self, **kwargs):
        pass

    def update(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass


class Award(models.Model):
    description = models.CharField(max_length=255)
    required_conquests = models.IntegerField()
    max_quantity = models.IntegerField()
    available_quantity = models.IntegerField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    conquests = models.ManyToManyField(Conquest, blank=True)

    objects = AwardManager()
