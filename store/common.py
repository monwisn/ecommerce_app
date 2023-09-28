import datetime

from django.db import models


class Timestamped(models.Model):
    created: datetime = models.DateTimeField(auto_now_add=True)
    updated: datetime = models.DateTimeField(auto_now=True)

    class Meta:
        abstract: bool = True
