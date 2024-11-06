from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    TIMEZONE_CHOICES = [
        ('UTC', 'UTC'),
        ('Europe/Paris', 'Europe/Paris'),
        # Ajoutez d'autres fuseaux horaires selon vos besoins
    ]
    
    LEVEL_CHOICES = [
        ('beginner', 'Débutant'),
        ('intermediate', 'Intermédiaire'),
        ('advanced', 'Avancé')
    ]
    
    timezone = models.CharField(max_length=50, choices=TIMEZONE_CHOICES, default='UTC')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    daily_goal = models.IntegerField(default=10)  # en minutes
    last_login_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)