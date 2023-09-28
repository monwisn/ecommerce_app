from datetime import datetime

from django.db import models


# Store Subscribers
class NewsletterUser(models.Model):
    email: models.EmailField = models.EmailField(max_length=80, unique=True)
    joined: datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Newsletter email: {self.email}'

