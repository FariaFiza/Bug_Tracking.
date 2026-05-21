from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'Normal User'),
        ('developer', 'Developer'),
        ('admin', 'Admin'),
    ]
    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('offline', 'Offline'),
    ]

    role         = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    bio          = models.TextField(blank=True)
    avatar_color = models.CharField(max_length=7, default='#4f46e5')
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='available')
    is_approved  = models.BooleanField(default=True)   # admin can ban
    skills       = models.CharField(max_length=200, blank=True, help_text="e.g. Python, Java, JavaScript")
    total_rating = models.FloatField(default=0.0)
    rating_count = models.IntegerField(default=0)

    def is_developer(self):
        return self.role == 'developer'

    def is_admin_user(self):
        return self.role == 'admin' or self.is_superuser

    def avg_rating(self):
        if self.rating_count == 0:
            return 0
        return round(self.total_rating / self.rating_count, 1)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"