from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

from api.models.event import Event


class UserManager(BaseUserManager):
    def create_user(self, name, username, password):
        user = self.model(name=name, username=username)
        user.set_password(password)
        user.save()

    def create_superuser(self, name, username, password):
        user = self.model(name=name, username=username)
        user.set_password(password)
        user.is_staff()
        user.is_superuser = True
        user.save()


class User(AbstractBaseUser):
    name = models.CharField(max_length=128)
    username = models.CharField(max_length=128, unique=True)
    is_admin = models.BooleanField(default=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    objects = UserManager()
    USERNAME_FIELD = 'username'
