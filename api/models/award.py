from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

from api.models import User
from api.models.conquest import Conquest
from api.models.event import Event


class AwardManager(models.Manager):
    def create(self, **kwargs):
        award = self.model(**kwargs)
        award.available_quantity = award.max_quantity
        award.save()
        return award

    def update(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass


class Award(models.Model):
    description = models.CharField(max_length=255)
    required_conquests = models.IntegerField()
    max_quantity = models.IntegerField()
    available_quantity = models.IntegerField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='awards')
    conquests = models.ManyToManyField(Conquest, blank=True)
    users = models.ManyToManyField(User, blank=True)

    objects = AwardManager()

    def __str__(self):
        return self.description
