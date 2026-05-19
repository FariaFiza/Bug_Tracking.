from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'Normal User'),
        ('developer', 'Developer'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    bio = models.TextField(blank=True)
    avatar_color = models.CharField(max_length=7, default='#6366f1')

    # New field to track free sessions for Normal Users
    free_sessions_remaining = models.IntegerField(default=2)

    @property
    def is_developer(self):
        return self.role == 'developer'

    @property
    def is_admin_user(self):
        return self.role == 'admin' or self.is_superuser

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"