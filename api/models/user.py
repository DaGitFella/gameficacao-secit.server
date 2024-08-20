from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

from api.models.activity import Activity
from api.models.award import Award
from api.models.event import Event


class UserManager(BaseUserManager):
    def create_user(self, name, username, password, email):
        user = self.model(name=name, username=username, email=email)
        user.set_password(password)
        user.save()

    def create_superuser(self, name, username, password, email):
        user = self.model(name=name, username=username, email=email)
        user.set_password(password)
        user.is_staff()
        user.is_superuser = True
        user.save()


class User(AbstractBaseUser):
    class Roles(models.TextChoices):
        ADMIN = "admin"
        VOLUNTEER = "voluntario"
        PRESENTER = "apresentador"
        COMMON = "comum"

    name = models.CharField(max_length=128)
    username = models.CharField(max_length=128, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=64, choices=Roles.choices, default=Roles.COMMON)
    events = models.ManyToManyField(Event, blank=True)
    activities = models.ManyToManyField(Activity, blank=True)
    awards = models.ManyToManyField(Award, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'username'
