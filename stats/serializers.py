from rest_framework import serializers
from .models import MeditationSession, UserStatistics, Achievement, UserAchievement

class MeditationSessionSerializer(serializers.ModelSerializer):
    duration = serializers.FloatField(read_only=True)

    class Meta:
        model = MeditationSession
        fields = ('id', 'user', 'meditation', 'started_at', 'ended_at',
                 'completed', 'duration', 'created_at')
        read_only_fields = ('created_at',)

class UserStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatistics
        fields = ('id', 'user', 'date', 'total_time', 'sessions_count',
                 'streak_days', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ('id', 'name', 'description', 'icon', 'condition_type',
                 'condition_value', 'created_at')
        read_only_fields = ('created_at',)

class UserAchievementSerializer(serializers.ModelSerializer):
    achievement = AchievementSerializer(read_only=True)

    class Meta:
        model = UserAchievement
        fields = ('id', 'user', 'achievement', 'achieved_at')
        read_only_fields = ('achieved_at',)