from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        raise NotImplementedError()
    def create_superuser(self):
        raise NotImplementedError()


class User(AbstractBaseUser):

    objects = UserManager()
