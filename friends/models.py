from django.db import models
from django.utils import timezone


class FriendsRecom(models.Model):
    created_date = models.DateTimeField(default=timezone.now)

