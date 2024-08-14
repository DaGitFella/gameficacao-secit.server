from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

from api.models.event import Event


class ActivityManager(models.Manager):
    def create(self, **kwargs):
        pass

    def update(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass


class Activity(models.Model):
    class PossibleTypes(models.TextChoices):
        PPMR = "painel-palestra-mesa-roda"
        PRESENTER = "apresentador"
        MINI_COURSE_or_MARKETING = "minicurso-desafio_marketing"
        QUESTION = "pergunta"
        PRESENTATION = "estande-sipex-integrador-desafio_marketing"
        MOCITEC = "networking-mociteczn"
        VOLUNTEER = "voluntario"

    stamps_amount = models.IntegerField()
    timestamp = models.DateTimeField()
    type = models.CharField(max_length=64, choices=PossibleTypes)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    objects = ActivityManager()
