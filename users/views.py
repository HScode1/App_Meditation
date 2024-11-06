from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Les utilisateurs normaux ne peuvent voir que leur profil
        if not self.request.user.is_staff:
            return self.queryset.filter(id=self.request.user.id)
        return self.queryset

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_daily_goal(self, request, pk=None):
        user = self.get_object()
        daily_goal = request.data.get('daily_goal')
        if daily_goal:
            user.daily_goal = daily_goal
            user.save()
            return Response({'status': 'daily goal updated'})
        return Response({'error': 'daily_goal is required'}, 
                       status=status.HTTP_400_BAD_REQUEST)