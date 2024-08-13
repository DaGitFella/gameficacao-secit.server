from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

from api.models.event import Event


class StampManager(models.Manager):
    def create(self, **kwargs):
        pass

    def update(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass


class Stamp(models.Model):
    icon = models.CharField(max_length=128)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    objects = StampManager()
