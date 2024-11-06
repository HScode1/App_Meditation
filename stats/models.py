from django.db import models
from users import User

# Create your models here.
class MeditationSession(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    meditation = models.ForeignKey('meditation.Meditation', on_delete=models.CASCADE)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()
    completed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def duration(self):
        return (self.ended_at - self.started_at).total_seconds() / 60

class UserStatistics(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    date = models.DateField()
    total_time = models.IntegerField(default=0)  # en minutes
    sessions_count = models.IntegerField(default=0)
    streak_days = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'date')

class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=100)
    condition_type = models.CharField(max_length=50)  # e.g., 'streak', 'total_time', 'sessions'
    condition_value = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class UserAchievement(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    achieved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'achievement')