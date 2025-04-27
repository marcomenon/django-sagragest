from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    theme = models.CharField(max_length=50, default='default')
    printer = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username

    @property
    def initials(self):
        if self.first_name and self.last_name:
            return f"{self.first_name[0]}{self.last_name[0]}".upper()
        elif self.first_name:
            return self.first_name[:2].upper()
        elif self.username:
            return self.username[:2].upper()
        return "U"
