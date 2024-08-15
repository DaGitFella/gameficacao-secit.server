from django.contrib.auth.base_user import BaseUserManager
from django.db import models

import api


class EventManager(models.Manager):
    def create(self, **kwargs):
        event = self.model(name=kwargs['name'], year=kwargs['year'], edition_number=kwargs['edition_number'])
        event.save()

        return event

    @staticmethod
    def update(instance, **kwargs):
        instance.name = kwargs['name']
        instance.year = kwargs['year']
        instance.edition_number = kwargs['edition_number']

        instance.save()

    @staticmethod
    def delete(instance):
        instance.delete()


class Event(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField()
    edition_number = models.IntegerField()

    objects = EventManager()
