from django.db import models

from api.models import User
from api.models.activity import Activity


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()


