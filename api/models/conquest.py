from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

from api.models.event import Event
from api.models.stamp import Stamp


class ConquestManager(models.Manager):
    def create(self, **kwargs):
        pass

    def update(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass


class Conquest(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    required_stamps = models.IntegerField()
    stamp = models.ForeignKey(Stamp, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    objects = ConquestManager()
