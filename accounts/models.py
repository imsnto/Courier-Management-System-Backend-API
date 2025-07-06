from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        DELIVERY_MAN = 'DELIVERY_MAN', 'Delivery Man'
        USER = 'USER', 'User'
    
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER
    )

    def __str__(self):
        return f"{self.username} ({self.role})"