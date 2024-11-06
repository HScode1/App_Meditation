from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from .models import (MeditationSession, UserStatistics, Achievement, 
                    UserAchievement)
from .serializers import (MeditationSessionSerializer, UserStatisticsSerializer,
                         AchievementSerializer, UserAchievementSerializer)

class MeditationSessionViewSet(viewsets.ModelViewSet):
    serializer_class = MeditationSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MeditationSession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        self._update_user_statistics(serializer.instance)

    def _update_user_statistics(self, session):
        date = session.started_at.date()
        stats, _ = UserStatistics.objects.get_or_create(
            user=session.user,
            date=date
        )
        
        # Mettre à jour les statistiques
        stats.total_time += session.duration
        stats.sessions_count += 1
        
        # Calculer le streak
        yesterday_stats = UserStatistics.objects.filter(
            user=session.user,
            date=date - timedelta(days=1)
        ).first()
        
        if yesterday_stats and yesterday_stats.streak_days > 0:
            stats.streak_days = yesterday_stats.streak_days + 1
        else:
            stats.streak_days = 1
            
        stats.save()
        
        # Vérifier les achievements
        self._check_achievements(session.user, stats)

    def _check_achievements(self, user, stats):
        # Exemple de vérification d'achievements
        achievements = Achievement.objects.all()
        for achievement in achievements:
            if achievement.condition_type == 'streak' and stats.streak_days >= achievement.condition_value:
                UserAchievement.objects.get_or_create(
                    user=user,
                    achievement=achievement
                )

class UserStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserStatisticsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserStatistics.objects.filter(user=self.request.user)

    @action(detail=False)
    def summary(self, request):
        current_date = timezone.now().date()
        start_of_month = current_date.replace(day=1)
        
        monthly_stats = self.get_queryset().filter(
            date__gte=start_of_month
        ).aggregate(
            total_time=Sum('total_time'),
            total_sessions=Sum('sessions_count')
        )
        
        current_streak = self.get_queryset().filter(
            date=current_date
        ).values_list('streak_days', flat=True).first() or 0

        return Response({
            'monthly_meditation_time': monthly_stats['total_time'] or 0,
            'monthly_sessions': monthly_stats['total_sessions'] or 0,
            'current_streak': current_streak,
        })

class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False)
    def my_achievements(self, request):
        user_achievements = UserAchievement.objects.filter(
            user=request.user
        ).select_related('achievement')
        serializer = UserAchievementSerializer(user_achievements, many=True)
        return Response(serializer.data)