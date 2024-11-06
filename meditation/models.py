from django.db import models

# Create your models here.
class MeditationType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Meditation(models.Model):
    LANGUAGE_CHOICES = [
        ('fr', 'Français'),
        ('en', 'English'),
        # Ajoutez d'autres langues selon vos besoins
    ]
    
    LEVEL_CHOICES = [
        ('beginner', 'Débutant'),
        ('intermediate', 'Intermédiaire'),
        ('advanced', 'Avancé')
    ]
    
    GENDER_CHOICES = [
        ('M', 'Homme'),
        ('F', 'Femme'),
        ('N', 'Neutre')
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    audio_url = models.URLField()
    duration = models.IntegerField(help_text="Durée en minutes")
    meditation_type = models.ForeignKey(MeditationType, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    narrator_gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    tags = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Favorite(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    meditation = models.ForeignKey(Meditation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'meditation')

