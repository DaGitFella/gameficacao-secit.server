from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, password, name, email):
        user = self.model(name=name, username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.is_active = True
        user.save()

        return user

    def create_superuser(self, username, password, email, name=None):
        user = self.create_user(username=username, password=password, name=name, email=email)
        user.role = User.Roles.ADMIN
        user.is_superuser = True
        user.is_active = True
        user.save()

        return user

    def update(self, instance, validated_data):
        instance.username = validated_data['username']
        instance.email = self.normalize_email(validated_data['email'])
        instance.name = validated_data['name']

        instance.set_password(validated_data['password'])
        instance.save()

        return instance

    def delete(self, user):
        self.filter(username=user.username).delete()

    def set_role(self, role: str, username: str):
        user = self.get(username=username)
        user.role = role
        user.save()


class User(AbstractBaseUser):
    class Roles(models.TextChoices):
        ADMIN = "admin"
        VOLUNTEER = "voluntario"
        PRESENTER = "apresentador"
        COMMON = "comum"

    name = models.CharField(max_length=128, blank=True)
    username = models.CharField(max_length=128, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=64, choices=Roles.choices, default=Roles.COMMON)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['email', 'name']
