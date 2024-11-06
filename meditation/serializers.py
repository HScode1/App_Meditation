from rest_framework import serializers
from .models import Meditation, MeditationType, Favorite

class MeditationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeditationType
        fields = '__all__'

class MeditationSerializer(serializers.ModelSerializer):
    meditation_type = MeditationTypeSerializer(read_only=True)
    meditation_type_id = serializers.PrimaryKeyRelatedField(
        queryset=MeditationType.objects.all(),
        write_only=True
    )

    class Meta:
        model = Meditation
        fields = ('id', 'title', 'description', 'audio_url', 'duration',
                 'meditation_type', 'meditation_type_id', 'level', 'language',
                 'narrator_gender', 'tags', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

class FavoriteSerializer(serializers.ModelSerializer):
    meditation = MeditationSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ('id', 'user', 'meditation', 'created_at')
        read_only_fields = ('created_at',)