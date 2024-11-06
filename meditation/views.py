from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Meditation, MeditationType, Favorite
from .serializers import (MeditationSerializer, MeditationTypeSerializer, 
                        FavoriteSerializer)

class MeditationTypeViewSet(viewsets.ModelViewSet):
    queryset = MeditationType.objects.all()
    serializer_class = MeditationTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'description']

class MeditationViewSet(viewsets.ModelViewSet):
    queryset = Meditation.objects.all()
    serializer_class = MeditationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['level', 'language', 'meditation_type', 'narrator_gender']
    search_fields = ['title', 'description', 'tags']

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        meditation = self.get_object()
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            meditation=meditation
        )
        return Response({'status': 'favorited' if created else 'already favorited'})

    @action(detail=True, methods=['post'])
    def unfavorite(self, request, pk=None):
        meditation = self.get_object()
        deleted, _ = Favorite.objects.filter(
            user=request.user,
            meditation=meditation
        ).delete()
        return Response({'status': 'unfavorited' if deleted else 'not favorited'})

    @action(detail=False)
    def favorites(self, request):
        favorites = Favorite.objects.filter(user=request.user)
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)